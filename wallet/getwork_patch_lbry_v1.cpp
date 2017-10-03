
/************ Xiao Lin's mod **************/
#include <openssl/ripemd.h>
#include <openssl/sha.h>
#include "wallet/wallet.h"
#include "utilmoneystr.h"
#include "consensus/merkle.h"
#include "uint256.h"
typedef map<uint256, pair<CBlock*, CScript> > mapNewBlock_t;
extern CWallet* pwalletMain;
inline uint32_t ByteReverse(uint32_t value)
{
    value = ((value & 0xFF00FF00) >> 8) | ((value & 0x00FF00FF) << 8);
    return (value<<16) | (value>>16);
}
int static FormatHashBlocks(void* pbuffer, unsigned int len)
{
  unsigned char* pdata = (unsigned char*)pbuffer;
  unsigned int blocks = 1 + ((len + 8) / 64);
  unsigned char* pend = pdata + 64 * blocks;
  memset(pdata + len, 0, 64 * blocks - len);
  pdata[len] = 0x80;
  unsigned int bits = len * 8;
  pend[-1] = (bits >> 0) & 0xff;
  pend[-2] = (bits >> 8) & 0xff;
  pend[-3] = (bits >> 16) & 0xff;
  pend[-4] = (bits >> 24) & 0xff;
  return blocks;
}
static const unsigned int pSHA256InitState[8] =
{0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19};
void SHA256Transform(void* pstate, void* pinput, const void* pinit)
{
  SHA256_CTX ctx;
  unsigned char data[64];
  SHA256_Init(&ctx);
  for (int i = 0; i < 16; i++)
  ((uint32_t*)data)[i] = ByteReverse(((uint32_t*)pinput)[i]);
  for (int i = 0; i < 8; i++)
  ctx.h[i] = ((uint32_t*)pinit)[i];
  SHA256_Update(&ctx, data, sizeof(data));
  for (int i = 0; i < 8; i++)
  ((uint32_t*)pstate)[i] = ctx.h[i];
}
void FormatHashBuffers(CBlock* pblock, char* pmidstate, char* pdata, char* phash1)
{
  struct
  {
    struct unnamed2
    {
      int nVersion;
      uint256 hashPrevBlock;
      uint256 hashMerkleRoot;
      unsigned int nTime;
      unsigned int nBits;
      unsigned int nNonce;
    }
    block;
    unsigned char pchPadding0[64];
    uint256 hash1;
    unsigned char pchPadding1[64];
  }
  tmp;
  memset(&tmp, 0, sizeof(tmp));
  tmp.block.nVersion       = pblock->nVersion;
  tmp.block.hashPrevBlock  = pblock->hashPrevBlock;
  tmp.block.hashMerkleRoot = pblock->hashMerkleRoot;
  tmp.block.nTime          = pblock->nTime;
  tmp.block.nBits          = pblock->nBits;
  tmp.block.nNonce         = pblock->nNonce;
  FormatHashBlocks(&tmp.block, sizeof(tmp.block));
  FormatHashBlocks(&tmp.hash1, sizeof(tmp.hash1));
  // Byte swap all the input buffer
  for (unsigned int i = 0; i < sizeof(tmp)/4; i++)
  ((unsigned int*)&tmp)[i] = ByteReverse(((unsigned int*)&tmp)[i]);

  // Precalc the first half of the first hash, which stays constant
  SHA256Transform(pmidstate, &tmp.block, pSHA256InitState);
  memcpy(pdata, &tmp.block, 128);
  memcpy(phash1, &tmp.hash1, 64);
}
// Key used by getwork miners.
// Allocated in InitRPCMining, free'd in ShutdownRPCMining
static CReserveKey* pMiningKey = NULL;
static CScript scriptPubKey;
void InitRPCMining()
{
    if (!pwalletMain)
        return;
    // getwork/getblocktemplate mining rewards paid here:
	if (pMiningKey==NULL)
	{
		pMiningKey = new CReserveKey(pwalletMain);
		// Create new block
		CPubKey pubkey;
		pMiningKey->GetReservedKey(pubkey);
		scriptPubKey = CScript() << ToByteVector(pubkey) << OP_CHECKSIG;
	}
	return;
}
void ShutdownRPCMining()
{
    if (!pMiningKey)
        return;
    delete pMiningKey; pMiningKey = NULL;
}

class submitblock_StateCatcher_G : public CValidationInterface
{
public:
    uint256 hash;
    bool found;
    CValidationState state;

    submitblock_StateCatcher_G(const uint256 &hashIn) : hash(hashIn), found(false), state() {}

protected:
    virtual void BlockChecked(const CBlock& block, const CValidationState& stateIn) {
        if (block.GetHash() != hash)
            return;
        found = true;
        state = stateIn;
    }
};

bool BIP22ValidationResult_G(const CValidationState& state)
{
    if (state.IsValid())
        return true;

    std::string strRejectReason = state.GetRejectReason();
    if (state.IsError())
        throw JSONRPCError(RPC_VERIFY_ERROR, strRejectReason);
    if (state.IsInvalid())
    {
        if (strRejectReason.empty())
            return false;
        return false;
    }
    // Should be impossible
    return true;
}
bool ProcessBlock(CValidationState &state, CNode* pfrom, CBlock* pblock)
{
	AssertLockHeld(cs_main);
	//LogPrintf("ProcessBlock() started\n");
	// Check for duplicate
	uint256 hash = pblock->GetHash();
    bool fBlockPresent = false;
    {
        LOCK(cs_main);
        BlockMap::iterator mi = mapBlockIndex.find(hash);
        if (mi != mapBlockIndex.end()) {
            CBlockIndex *pindex = mi->second;
            if (pindex->IsValid(BLOCK_VALID_SCRIPTS))
                return error("ProcessBlock() : duplicate");
            if (pindex->nStatus & BLOCK_FAILED_MASK)
                return error("ProcessBlock() : duplicate-invalid");
            // Otherwise, we might only have the header - process the block before returning
            fBlockPresent = true;
        }
    }

    submitblock_StateCatcher_G sc(pblock->GetHash());
    RegisterValidationInterface(&sc);
    bool fAccepted = ProcessNewBlock(state, Params(), NULL, pblock, true, NULL);
    UnregisterValidationInterface(&sc);
    if (fBlockPresent)
    {
        if (fAccepted && !sc.found)
            return true;
        return true;
    }
    if (!sc.found)
        return true;
	bool result=BIP22ValidationResult_G(sc.state);
	if(!result)
	{
		return error("ProcessBlock() : AcceptBlock FAILED");
	}
	LogPrintf("ProcessBlock: ACCEPTED\n");
    return true;
}
bool CheckWork(CBlock* pblock, CWallet& wallet, CReserveKey& reservekey)
{
  uint256 hashPoW = pblock->GetHash();
  uint256 hashTarget = ArithToUint256(arith_uint256().SetCompact(pblock->nBits));
  uint256 hashBlock = pblock->GetHash();
  //// debug print
  LogPrintf("Wallet mining:\n");
  LogPrintf("proof-of-work found  \n  block-hash: %s\n  pow-hash: %s\ntarget: %s\n",
  hashBlock.GetHex(),
  hashPoW.GetHex(),
  hashTarget.GetHex());
  LogPrintf("generated %s\n", FormatMoney(pblock->vtx[0].vout[0].nValue));
  // Found a solution
  {
    LOCK(cs_main);
    if (pblock->hashPrevBlock != chainActive.Tip()->GetBlockHash())
    return error("Wallet mining : generated block is stale");
    // Remove key from key pool
    reservekey.KeepKey();
    // Track how many getdata requests this block gets
    {
      LOCK(wallet.cs_wallet);
      wallet.mapRequestCount[pblock->GetHash()] = 0;
    }
    // Process this block the same as if we had received it from another node
    CValidationState state;
    if (!ProcessBlock(state, NULL, pblock))
    return error("Wallet mining : ProcessBlock, block not accepted");
  }
  return true;
}


UniValue getwork(const UniValue& params, bool fHelp)
{
	InitRPCMining();
    if (fHelp || params.size() > 1){
        throw runtime_error(
            "getwork ( \"data\" )\n"
            "\nIf 'data' is not specified, it returns the formatted hash data to work on.\n"
            "If 'data' is specified, tries to solve the block and returns true if it was successful.\n"
            "\nArguments:\n"
            "1. \"data\"       (string, optional) The hex encoded data to solve\n"
            "\nResult (when 'data' is not specified):\n"
            "{\n"
            "  \"midstate\" : \"xxxx\",   (string) The precomputed hash state after hashing the first half of the data (DEPRECATED)\n" // deprecated
            "  \"data\" : \"xxxxx\",      (string) The block data\n"
            "  \"hash1\" : \"xxxxx\",     (string) The formatted hash buffer for second hash (DEPRECATED)\n" // deprecated
            "  \"target\" : \"xxxx\"      (string) The little endian hash target\n"
            "}\n"
            "\nResult (when 'data' is specified):\n"
            "true|false       (boolean) If solving the block specified in the 'data' was successfull\n"
            "\nExamples:\n"
            + HelpExampleCli("getwork", "")
            + HelpExampleRpc("getwork", "")
	);}
	
    if (IsInitialBlockDownload())
        throw JSONRPCError(RPC_CLIENT_IN_INITIAL_DOWNLOAD, "This wallet is downloading blocks...");

    static mapNewBlock_t mapNewBlock;    // FIXME: thread safety
    static vector<CBlockTemplate*> vNewBlockTemplate;

    if (params.size() == 0)
    {
        // Update block
        static unsigned int nTransactionsUpdatedLast;
        static CBlockIndex* pindexPrev;
        static int64_t nStart;
        static CBlockTemplate* pblocktemplate;
        if (pindexPrev != chainActive.Tip() ||
            (mempool.GetTransactionsUpdated() != nTransactionsUpdatedLast && GetTime() - nStart > 60))
        {
            if (pindexPrev != chainActive.Tip())
            {
                // Deallocate old blocks since they're obsolete now
                mapNewBlock.clear();
                for (std::vector<CBlockTemplate*>::size_type i=0;i!=vNewBlockTemplate.size();i++)
				{
                    delete vNewBlockTemplate[i];
				}
                vNewBlockTemplate.clear();
            }

            // Clear pindexPrev so future getworks make a new block, despite any failures from here on
            pindexPrev = NULL;

            // Store the pindexBest used before CreateNewBlock, to avoid races
            nTransactionsUpdatedLast = mempool.GetTransactionsUpdated();
            CBlockIndex* pindexPrevNew = chainActive.Tip();
            nStart = GetTime();
			
			pblocktemplate=CreateNewBlock(Params(), scriptPubKey);
            if (!pblocktemplate)
                throw JSONRPCError(RPC_OUT_OF_MEMORY, "Out of memory");
            vNewBlockTemplate.push_back(pblocktemplate);
            // Need to update only after we know CreateNewBlock succeeded
            pindexPrev = pindexPrevNew;
        }
        CBlock* pblock = &(vNewBlockTemplate.back()->block); // pointer for convenience

        // Update nTime
		const Consensus::Params& consensusParams = Params().GetConsensus();
        UpdateTime(pblock, consensusParams, pindexPrev);
        pblock->nNonce = 0;

        // Update nExtraNonce
            LOCK(cs_main);
        static unsigned int nExtraNonce = 0;
        IncrementExtraNonce(pblock, pindexPrev, nExtraNonce);

        // Save
        mapNewBlock[pblock->hashMerkleRoot] = make_pair(pblock, pblock->vtx[0].vin[0].scriptSig);

        // Pre-build hash buffers
        char pmidstate[32];
        char pdata[128];
        char phash1[64];
        FormatHashBuffers(pblock, pmidstate, pdata, phash1);
        uint256 hashTarget = ArithToUint256(arith_uint256().SetCompact(pblock->nBits));

        UniValue result(UniValue::VOBJ);
        result.push_back(Pair("midstate", HexStr(BEGIN(pmidstate), END(pmidstate)))); // deprecated
        result.push_back(Pair("data",     HexStr(BEGIN(pdata), END(pdata))));
        result.push_back(Pair("hash1",    HexStr(BEGIN(phash1), END(phash1)))); // deprecated
        result.push_back(Pair("target",   HexStr(BEGIN(hashTarget), END(hashTarget))));
        return result;
    }
    else
    {
		
        // Parse parameters
        vector<unsigned char> vchData = ParseHex(params[0].get_str());
        if (vchData.size() != 128)
            throw JSONRPCError(RPC_INVALID_PARAMETER, "Invalid parameter");
        CBlock* pdata = (CBlock*)&vchData[0];
		
		
        // Byte reverse
        for (int i = 0; i < 128/4; i++)
            ((unsigned int*)pdata)[i] = ByteReverse(((unsigned int*)pdata)[i]);
		
        // Get saved block
        if (!mapNewBlock.count(pdata->hashMerkleRoot))
            return false;
        CBlock* pblock = mapNewBlock[pdata->hashMerkleRoot].first;
        pblock->nTime = pdata->nTime;
        pblock->nNonce = pdata->nNonce;
        //CMutableTransaction txCoinbase(*pblock->vtx[0]);
        //txCoinbase.vin[0].scriptSig = mapNewBlock[pdata->hashMerkleRoot].second;
		//pblock->vtx[0] = MakeTransactionRef(std::move(txCoinbase));
        pblock->hashMerkleRoot = BlockMerkleRoot(*pblock);
        assert(pwalletMain != NULL);
        return CheckWork(pblock, *pwalletMain, *pMiningKey);
    }
}
/*************Xiao Lin's mod ends *************/

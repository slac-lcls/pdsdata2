#ifndef Pds_Eb_EbAppBase_hh
#define Pds_Eb_EbAppBase_hh

#include "eb.hh"
#include "EventBuilder.hh"
#include "EbLfServer.hh"

#include <cstdint>
#include <cstddef>
#include <string>
#include <array>
#include <vector>


namespace XtcData {
  class Dgram;
  class TimeStamp;
};

namespace Pds {
  namespace Eb {

    class EbLfLink;
    class EbEvent;

    class EbAppBase : public EventBuilder
    {
    public:
      EbAppBase(const EbParams& prms,
                const uint64_t  duration,
                const unsigned  maxEntries,
                const unsigned  maxBuffers);
      virtual ~EbAppBase() {}
    public:
      const uint64_t&  rxPending() const { return _transport.pending(); }
      int              checkEQ()  { return _transport.pollEQ(); }
    public:
      int              connect(const EbParams&);
      int              process();
      void             shutdown();
    public:                          // For EventBuilder
      virtual void     fixup(Pds::Eb::EbEvent* event, unsigned srcId);
      virtual uint64_t contracts(const XtcData::Dgram* contrib,
                                 uint64_t& receivers) const;
    private:                           // Arranged in order of access frequency
      unsigned                 _groups;
      std::array<uint64_t, 16> _contracts;
      std::array<uint64_t, 16> _receivers;
      Pds::Eb::EbLfServer      _transport;
      std::vector<EbLfLink*>   _links;
      size_t                   _trSize;
      size_t                   _maxTrSize;
      std::vector<size_t>      _maxBufSize;
      unsigned                 _maxBuffers;
      //EbDummyTC                _dummy;   // Template for TC of dummy contributions  // Revisit: ???
      unsigned                 _verbose;
    private:
      void*                    _region;
      uint64_t                 _contributors;
      unsigned                 _id;
    };
  };
};

#endif


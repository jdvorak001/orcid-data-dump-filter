
ns = {
    "activities": "http://www.orcid.org/ns/activities",
    "address": "http://www.orcid.org/ns/address",
    "bulk": "http://www.orcid.org/ns/bulk",
    "common": "http://www.orcid.org/ns/common",
    "deprecated": "http://www.orcid.org/ns/deprecated",
    "education": "http://www.orcid.org/ns/education",
    "email": "http://www.orcid.org/ns/email",
    "employment": "http://www.orcid.org/ns/employment",
    "error": "http://www.orcid.org/ns/error",
    "external-identifier": "http://www.orcid.org/ns/external-identifier",
    "funding": "http://www.orcid.org/ns/funding",
    "history": "http://www.orcid.org/ns/history",
    "internal": "http://www.orcid.org/ns/internal",
    "keyword": "http://www.orcid.org/ns/keyword",
    "other-name": "http://www.orcid.org/ns/other-name",
    "peer-review": "http://www.orcid.org/ns/peer-review",
    "person": "http://www.orcid.org/ns/person",
    "personal-details": "http://www.orcid.org/ns/personal-details",
    "preferences": "http://www.orcid.org/ns/preferences",
    "record": "http://www.orcid.org/ns/record",
    "researcher-url": "http://www.orcid.org/ns/researcher-url",
    "work": "http://www.orcid.org/ns/work"
}

my_country = "CZ"

def match( xml_root ):
    "given a xml root element, it returns True when the profile matches your condition"
    
    x1 = xml_root.findall( 'person:person/address:addresses/address:address/address:country[ . = "%s" ]' % my_country, ns )
    x2 = xml_root.findall( 'activities:activities-summary/activities:educations/education:education-summary/education:organization/common:address/common:country[ . = "%s" ]' % my_country, ns )
    x3 = xml_root.findall( 'activities:activities-summary/activities:employments/employment:employment-summary/employment:organization/common:address/common:country[ . = "%s" ]' % my_country, ns )
    return x1 or x2 or x3

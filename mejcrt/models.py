'''
Created on 08/12/2015

@author: Iuri Diniz <iuridiniz@gmail.com>
'''
from google.appengine.ext import ndb
from utils import onlynumbers, iconv, tokenize

# Models
blood_types = ('A+', 'B+', 'AB+', "O+", 'A-', 'B-', 'AB-', "O-")

class Patient(ndb.Model):
    name = ndb.StringProperty(indexed=False, required=True)
    code = ndb.StringProperty(indexed=True, required=True, validator=onlynumbers)
    blood_type = ndb.StringProperty(indexed=False, required=True, choices=blood_types)
    type_ = ndb.StringProperty(indexed=False, required=True,
        choices=["RN", "G", "O"])

    name_tags = ndb.ComputedProperty(lambda self: self._gen_tokens_for_name(self.name), repeated=True)
    code_tags = ndb.ComputedProperty(lambda self: self._gen_tokens_for_code(self.code), repeated=True)

    def _gen_tokens_for_name(self, name):
        return list(tokenize(iconv(name.lower()), minimum=4, maximum=4))
    def _gen_tokens_for_code(self, code):
        return list(tokenize(iconv(code.lower())))

class BloodBag(ndb.Model):
    type_ = ndb.StringProperty(indexed=False, required=True, choices=blood_types)
    content = ndb.StringProperty()

class Transfusion(ndb.Model):
    patient = ndb.StructuredProperty(Patient)
    nhh_code = ndb.StringProperty(indexed=True, required=True, validator=onlynumbers)
    date = ndb.DateProperty(indexed=True, required=True)
    local = ndb.StringProperty(indexed=False, required=True,
        choices=["unidade-a", "unidade-b", 'unidade-b4', 'alto-risco',
                 'uti-neonatal', 'uti-materna', 'sem-registro'])
    bags = ndb.LocalStructuredProperty(BloodBag, repeated=True)
    tags = ndb.StringProperty(repeated=True, indexed=False,
        choices=['rt', "ficha-preenchida", "carimbo-plantao",
                 "carimbo-nhh", "anvisa"])
    text = ndb.TextProperty(required=False)

    added_at = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    updated_at = ndb.DateTimeProperty(auto_now=True, indexed=False)
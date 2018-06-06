import requests
import json
import pyforms
from   pyforms          import BaseWidget
from   pyforms.Controls import ControlText
from   pyforms.Controls import ControlButton
from pyforms.Controls import ControlTextArea
from pyforms.Controls import ControlCombo

def getClinVarObjects(data):
    result = []
    if isinstance(data, list):
        for element in data:
            if 'clinvar' in element : result.append(element['clinvar'])
    else:
        if 'clinvar' in data: result.append(data['clinvar'])
    return result

def getClinicalSignificance(rsid):
    basic_call = 'http://myvariant.info/v1/variant/'
    r = requests.get(basic_call+rsid)

    data = json.loads(r.text)
    
    result = []
    clinvar = getClinVarObjects(data)
    rcvs = []
    for element in clinvar:
        rcv = element['rcv']
        if isinstance(rcv, list):
            for element in rcv:
                result.append(element['clinical_significance'])
        else:
            result.append(rcv['clinical_significance'])
    if len(result) == 0: result.append('.')
    return ';'.join(result)

def getEnsemblResult(uri):
    r = requests.get(uri)
    return r.text

class SimpleExample1(BaseWidget):

    def __init__(self):
        super(SimpleExample1,self).__init__('my_variant_api')

        #init clinvar
        self._clinvariants     = ControlTextArea('rsvariants', 'rs12315123')
        self._clinbutton        = ControlButton('Press this button')
        self._clinresult = ControlTextArea('result')

        self._clinbutton.value = self.__clinbuttonAction
        #init flanking site
        self._flancchrom = ControlText('chrom')
        self._flancpos = ControlText('pos')
        self._flancthree = ControlText('expand_3prime',300)
        self._flancfive = ControlText('expand_5prime',300)
        self._flancassembly = ControlCombo('assembly')
        self._flancassembly.add_item('GRCh37')
        self._flancassembly.add_item('GRCh38')
        self._flancbutton = ControlButton('Press this button')
        self._flancresult = ControlTextArea('result')
        self._flancbutton.value = self.__flancbuttonAction

        self.formset = [{"Clinvar":('_clinvariants','_clinbutton','_clinresult'),
                "Flanking Site":[('_flancchrom','_flancpos','_flancthree','_flancfive','_flancassembly'),'_flancbutton','_flancresult']}]

    def __clinbuttonAction(self):
        results = []
        for rsid in self._clinvariants.value.split('\n'):
            clinsig = getClinicalSignificance(rsid)
            results.append(clinsig)
        self._clinresult.value = '\n'.join(results)

    def __flancbuttonAction(self):
        chrom = self._flancchrom.value
        pos = self._flancpos.value
        five = self._flancfive.value
        three = self._flancthree.value
        assembly = self._flancassembly.value
        uri = 'http://grch37.rest.ensembl.org/sequence/region/human/'+chrom+':'+pos+'..'+pos+':1?expand_3prime='+three+'&expand_5prime='+five+'&content-type=text/plain'
        site = getEnsemblResult(uri)
        fiveString = site[:int(five)]
        threeString = site[-int(three):]
        current = site[int(five):int(five)+1]
        self._flancresult.value = fiveString+'\n'+current+'\n'+threeString

#Execute the application
if __name__ == "__main__":   pyforms.start_app( SimpleExample1 )



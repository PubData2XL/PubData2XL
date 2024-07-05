# sendemail/forms.py
import re
from django import forms
PMID_REGEX = '^\d{1,8}$'   


class GetPMIDsForm(forms.Form):
    pmids = forms.CharField(label='PMIDs', required=True, error_messages={'required': 'At least one PMID is required.'}, widget=forms.Textarea(attrs={'placeholder': 'One PMID per row.'}))

    def clean_pmids(self):
        pmds = self.cleaned_data.get('pmids')
        for pmd in pmds.strip().split('\r\n'):
            pmd = pmd.strip()
            if not re.match(PMID_REGEX, pmd) or int(pmd) > 45000000 or int(pmd) == 0:
                raise forms.ValidationError(pmd + " is not a valid PMID.")
        #raise forms.ValidationError(p)
        return pmds
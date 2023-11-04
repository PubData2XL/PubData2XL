javascript:(
    function(){
        function goToPubMed2XL(pmids){
            if (pmids != "") {window.open("https://www.pubmed2xl.com/" + pmids, '_blank');} 
            else {alert("Hmm, looks like you didn't select any records, or did you?");}
        }
        var pmids;
        switch (document.domain) {
            case "ovidsp.dc2.ovid.com":pmids = $("td.titles-checkbox input:checked").parent().siblings().find("div.article-ui").map(function(){return $(this).text().match(/([0-9]+)/)[0]; }).get().join(",");
            goToMPubMed2XL(pmids);
            break;
            case "www.ncbi.nlm.nih.gov":pmids = jQuery("div.rprtnum input:checked").map(function(){ return this.value; }).get().join(",");
            goToPubMed2XL(pmids);
            break;
            case "pubmed.ncbi.nlm.nih.gov":pmids = $("div#search-results section.search-results-list article input.search-result-selector:checked").map(function(){ return this.value; }).get().join(",");
            goToPubMed2XL(pmids);
            break;
            default:alert("Hmm, looks like you are not on a supported site, or are you?");
        }
    }
)()

javascript:(function(){function goToPubMed2XL(pmids){if (pmids != "") {window.open("https://www.pubmed2xl.com/" + pmids, '_blank');}else {alert("Hmm, looks like you didn't select any records, or did you?");}}var pmids;switch (document.domain) {case "ovidsp.dc2.ovid.com":pmids = $("td.titles-checkbox input:checked").parent().siblings().find("div.article-ui").map(function(){return $(this).text().match(/([0-9]+)/)[0]; }).get().join(",");goToMPubMed2XL(pmids);break;case "www.ncbi.nlm.nih.gov":pmids = jQuery("div.rprtnum input:checked").map(function(){ return this.value; }).get().join(",");goToPubMed2XL(pmids);break;case "pubmed.ncbi.nlm.nih.gov":pmids = $("div#search-results section.search-results-list article input.search-result-selector:checked").map(function(){ return this.value; }).get().join(",");goToPubMed2XL(pmids);break;default:alert("Hmm, looks like you are not on a supported site, or are you?");}})()


javascript:(function()%7Bfunction goToPubMed2XL(pmids)%7Bif (pmids !%3D "") %7Bwindow.location.href %3D "https://www.pubmed2xl.com%2F" %2B pmids%3B%7D else %7Balert("Hmm%2C looks like you didn't select any records%2C or did you%3F")%3B%7D%7Dvar  pmids%3Bswitch (document.domain) %7Bcase "ovidsp.dc2.ovid.com"%3Apmids %3D %24("td.titles-checkbox input%3Achecked").parent().siblings().find("div.article-ui").map(function()%7B return %24(this).text().match(%2F(%5B0-9%5D%2B)%2F)%5B0%5D%3B %7D).get().join("%2C")%3BgoToMPubMed2XL(pmids)%3Bbreak%3Bcase "www.ncbi.nlm.nih.gov"%3Apmids %3D jQuery("div.rprtnum input%3Achecked").map(function()%7B return this.value%3B %7D).get().join("%2C")%3BgoToPubMed2XL(pmids)%3Bbreak%3Bcase "pubmed.ncbi.nlm.nih.gov"%3Apmids %3D %24("div%23search-results section.search-results-list article input.search-result-selector%3Achecked").map(function()%7B return this.value%3B %7D).get().join("%2C")%3BgoToPubMed2XL(pmids)%3Bbreak%3Bdefault%3Aalert("Hmm%2C looks like you are not on a supported site%2C or are you%3F")%3B%7D%7D)()
const textarea = document.getElementById("id_pmids");
const counter = document.getElementById('count');
const link_ids = ['left_link_url', 'right_link_url','logo_link_url'];

const baseURL_regex = ".*\/";

textarea.addEventListener('load', rowsCounter(textarea, counter, link_ids, baseURL_regex));
textarea.addEventListener('input', rowsCounter(textarea, counter, link_ids, baseURL_regex));
// Count how many rows (pmids) in textarea.
function rowsCounter(textarea, counter, link_ids, regex) {
  const text = textarea.value.replace(/[^0-9\n]/g, '').replace("/",",");
  const lines = text.split("\n");
  const filtered = lines.filter(elm => elm);
  console.log(filtered);
  textarea.value = filtered.join('\r\n');
  textarea.parentNode.dataset.replicatedValue = textarea.value;
  const count = filtered.length;
  row = " rows"
  if (count <= 1){
    row = " row"
  }
  counter.innerHTML = count + row;
  // This update the links based on page context.
  // e.g. if in excel page show XML link, but if in XML page show excel link
  for (let i = 0; i < link_ids.length; i++) {
    // console.log(link_ids[i]);
    var anchor = document.getElementById(link_ids[i]);
    var link = anchor.getAttribute("href").match(regex);
    anchor.setAttribute("href", link + filtered);
  }
}
// Set blinking caret at the end on load
document.addEventListener('load', setCaretPosition(textarea, -1, -1));
function setCaretPosition(ctrl, start, end) {
  // IE >= 9 and other browsers
  if (ctrl.setSelectionRange) {
      ctrl.focus();
      ctrl.setSelectionRange(start, end);
  }
  // IE < 9 
  else if (ctrl.createTextRange) {
      var range = ctrl.createTextRange();
      range.collapse(true);
      range.moveEnd('character', end);
      range.moveStart('character', start);
      range.select();
  }
}

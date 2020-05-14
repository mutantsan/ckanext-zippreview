var frame = this.frameElement;
var div = this.parent.document.createElement('div')
div.setAttribute("id", "zip-warning");
frame.parentNode.before(div);
frame.onload = function() {
    div.remove();
    frame.style.minHeight = frame.contentDocument.body.clientHeight + "px";
}

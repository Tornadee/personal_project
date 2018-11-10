var keyRightDown = false;
var keyLeftDown = false;
document.onkeydown = function(e) {
  if (e.keyCode == 37) {
    keyLeftDown = true;
  }
  if (e.keyCode == 39) {
    keyRightDown = true;
  }
}
document.onkeyup = function(e) {
  if (e.keyCode == 37) {
    keyLeftDown = false;
  }
  if (e.keyCode == 39) {
    keyRightDown = false;
  }
}

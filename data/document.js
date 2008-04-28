function sleep(millisecondi) {
  var now = new Date();
  var exitTime = now.getTime() + millisecondi;

  while(true) {
    now = new Date();
    if(now.getTime() > exitTime) return;
  }
}

function exec_wait_msg(func) {
  location.href = 'http://cmd/msg/add/wait';
  func();
  sleep(60)
  location.href = 'http://cmd/msg/remove/wait';
}

function font_size(percent) {
  $('p,h1,h2,h3,h4,h5,h6,span,div').each( function() {
    $(this).css('font-size', parseFloat($(this).css('font-size'), 10) * percent)
  });
}

function increaseFont() {
  exec_wait_msg(function() { font_size(1.1) });  
}

function decreaseFont() {
  exec_wait_msg(function() { font_size(0.9) });
  font_size(0.9)
}

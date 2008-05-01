
/*##############################################################################
# ODF Mobile
#
# License: GPL
# Copyright (c) 2008 ODF Mobile team
#
#
# Last Modified: 2008-05-1 12:24
#
# License Information:
#
# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# at your option.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
##############################################################################*/

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
  alert('teste');
}

function decreaseFont() {
  exec_wait_msg(function() { font_size(0.9) });
}

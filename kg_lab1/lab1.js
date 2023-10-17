var cmyk_slider = document.getElementsByClassName("cmyk-slider");
var cmyk_in = document.getElementsByClassName("cmyk-in");
var rgb_slider = document.getElementsByClassName("rgb-slider");
var rgb_in = document.getElementsByClassName("rgb-in");
var hsv_slider = document.getElementsByClassName("hsv-slider");
var hsv_in = document.getElementsByClassName("hsv-in");
var chooser = document.getElementById("chooser");
var c = document.getElementById("canvas");
var ctx = c.getContext("2d");
changeCanvas(0,0,0);
function changeCanvas(r,g,b){
    ctx.fillStyle = 'rgb(' + r + ', ' + g + ', ' + b + ')';
    ctx.fillRect(0,0, 150, 150);   
}

const hexToRgb = (hex) => {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return [r,g,b];
}

function chooseColor() {
    setRgb.apply(this, hexToRgb(chooser.value));
    rgbSlider();
}

function setCmyk(c,m,y,k){
    cmyk_slider[0].value = c;
    cmyk_slider[1].value = m;
    cmyk_slider[2].value = y;
    cmyk_slider[3].value = k;
    cmyk_in[0].value = c;
    cmyk_in[1].value = m;
    cmyk_in[2].value = y;
    cmyk_in[3].value = k;
}

function setRgb(r,g,b){
    rgb_slider[0].value = r;
    rgb_slider[1].value = g;
    rgb_slider[2].value = b;
    rgb_in[0].value = r;
    rgb_in[1].value = g;
    rgb_in[2].value = b;
}

function setHsv(h,s,v){
    hsv_slider[0].value = h;
    hsv_slider[1].value = s;
    hsv_slider[2].value = v;
    hsv_in[0].value = h;
    hsv_in[1].value = s;
    hsv_in[2].value = v;   
}

function getCMYK(){
    var c = cmyk_slider[0].value;
    var m = cmyk_slider[1].value;
    var y = cmyk_slider[2].value;
    var k = cmyk_slider[3].value;
    return [c,m,y,k];
}

function getCMYKin(){
    var c = cmyk_in[0].value;
    var m = cmyk_in[1].value;
    var y = cmyk_in[2].value;
    var k = cmyk_in[3].value;
    return [c,m,y,k];
}

function getRGB(){
    var r = rgb_slider[0].value;
    var g = rgb_slider[1].value;
    var b = rgb_slider[2].value;
    return [r,g,b];
}

function getRGBin(){
    var r = rgb_in[0].value;
    var g = rgb_in[1].value;
    var b = rgb_in[2].value;
    return [r,g,b];
}

function getHSV(){
    var h = hsv_slider[0].value;
    var s = hsv_slider[1].value;
    var v = hsv_slider[2].value;
    return [h,s,v];
}

function getHSVin(){
    var h = hsv_in[0].value;
    var s = hsv_in[1].value;
    var v = hsv_in[2].value;
    return [h,s,v];
}


function changeFromRgb(r,g,b){
    setRgb(r,g,b);
    setCmyk.apply(this, rgbToCmyk(r,g,b));
    setHsv.apply(this, rgbToHsv(r,g,b));
}

function changeFromHsv(h,s,v){
    setHsv(h,s,v);
    setCmyk.apply(this, hsvToCmyk(h,s,v));
    setRgb.apply(this, hsvToRgb(h,s,v));
}

function changeFromCmyk(){
    setCmyk.apply(this, getCMYK());
    setRgb.apply(this, cmykToRgb());
    setHsv.apply(this, cmykToHsv());
}

function cmykToRgb(){
    var cmyk = getCMYK();
    var r = 255 * (1 - cmyk[0]) * (1 - cmyk[3]);
    var g = 255 * (1 - cmyk[1]) * (1 - cmyk[3]);
    var b = 255 * (1 - cmyk[2]) * (1 - cmyk[3]);
    return [Math.round(r),Math.round(g),Math.round(b)];
}

function rgbToHsv(r, g, b) {
    r /= 255, g /= 255, b /= 255;
  
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, v = max;
  
    var d = max - min;
    s = max == 0 ? 0 : d / max;
  
    if (max == min) {
      h = 0;
    } else {
      switch (max) {
        case r: h = (g - b) / d + (g < b ? 6 : 0); break;
        case g: h = (b - r) / d + 2; break;
        case b: h = (r - g) / d + 4; break;
      }
  
      h /= 6;
    }
  
    return [Math.round(h*360), s.toFixed(2), v.toFixed(2)];
  }
  
  function hsvToRgb(h, s, v) {
    h = h/360;
    var r, g, b;
    var i = Math.floor(h * 6);
    var f = h * 6 - i;
    var p = v * (1 - s);
    var q = v * (1 - f * s);
    var t = v * (1 - (1 - f) * s);
  
    switch (i % 6) {
      case 0: r = v, g = t, b = p; break;
      case 1: r = q, g = v, b = p; break;
      case 2: r = p, g = v, b = t; break;
      case 3: r = p, g = q, b = v; break;
      case 4: r = t, g = p, b = v; break;
      case 5: r = v, g = p, b = q; break;
    }
  
    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
  }
function cmykToHsv(){
    var rgb = cmykToRgb();
    var hsv = rgbToHsv(rgb[0], rgb[1], rgb[2]);
    return hsv;
}

function hsvToCmyk(h,s,v){
    var rgb = hsvToRgb(h,s,v);
    var cmyk = rgbToCmyk(rgb[0], rgb[1], rgb[2]);
    return cmyk;
}

function rgbToCmyk(r,g,b){
    var k = Math.min(1 - r/255, 1 - g/255, 1 - b/255);
    var c = (1 - r/255 - k)/(1 - k);
    var m = (1 - g/255 - k)/(1 - k);
    var y = (1 - b/255 - k)/(1 - k);
    return [c.toFixed(2),m.toFixed(2),y.toFixed(2),k.toFixed(2)];
}

function cmykSlider(){
    changeFromCmyk.apply(this, getCMYK());
    changeCanvas(rgb_slider[0].value, rgb_slider[1].value, rgb_slider[2].value);
}

function cmykIn(){
    setCmyk.apply(this,getCMYKin());
    changeFromCmyk.apply(this,getCMYKin());
    changeCanvas(rgb_in[0].value, rgb_in[1].value, rgb_in[2].value);
}

function rgbSlider(){
    changeFromRgb.apply(this, getRGB());
    changeCanvas(rgb_slider[0].value, rgb_slider[1].value, rgb_slider[2].value);
}

function rgbIn(){
    setRgb.apply(this,getRGBin());
    changeFromRgb.apply(this,getRGBin());
    changeCanvas(rgb_in[0].value, rgb_in[1].value, rgb_in[2].value);
}

function hsvIn(){
    setHsv.apply(this,getHSVin());
    changeFromHsv.apply(this,getHSVin());
    changeCanvas(rgb_in[0].value, rgb_in[1].value, rgb_in[2].value);
}
function hsvSlider(){
    changeFromHsv.apply(this, getHSV());
    changeCanvas(rgb_slider[0].value, rgb_slider[1].value, rgb_slider[2].value);
}

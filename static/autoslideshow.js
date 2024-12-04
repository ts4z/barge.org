"use strict";

// based on https://www.w3schools.com/howto/howto_js_slideshow.asp

let slideDecks = {};
let slideClassToIndex = {};

/* Class the members of each slideshow group with different CSS classes */

function getSlideIndex(clazz) {
  let slides = document.getElementsByClassName(clazz);
  let i = slideClassToIndex[clazz];
  if (typeof i === 'undefined') {
    return 0;
  } else {
    return i;
  }
}

function setSlideIndex(clazz, i) {
  let slides = document.getElementsByClassName(clazz);
  if (i < 0) {
    slideClassToIndex[clazz] = slides.length - 1;   // wrap left
  } else if (i >= slides.length) {
    slideClassToIndex[clazz] = 0;
  } else {
    slideClassToIndex[clazz] = i;
  }
  return slideClassToIndex[clazz];
}


function stepSlide(k, step) {
  let was = getSlideIndex(k);
  let is = setSlideIndex(k, was + step);
  let slides = document.getElementsByClassName(k);
  slides[was].style.display = "none";
  slides[is].style.display = "block";
}

function autoRotate(k, interval) {
  stepSlide(k, 1);
  setTimeout(() => autoRotate(k, interval), interval);
}

function initSlides(k, interval, delay) {
  let slides = document.getElementsByClassName(k);
  let start = Math.floor(Math.random() * slides.length);
  stepSlide(k, start);
  setTimeout(() =>
    setTimeout(() => autoRotate(k, interval), interval),
    delay);
}

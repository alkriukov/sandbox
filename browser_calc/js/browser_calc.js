window.onload = function() {
  var calcArea = document.getElementById("calc_area");

  calcArea.addEventListener('keyup', (e) => {
    var key = e.keyCode || e.which;
    let enterKeyCode = 13;
    if (key == enterKeyCode) {
      calcArea.value += calculate(calcArea.value);
    };
  });
};

function calculate(rawText) {
  equationText = searchBottomEquation(rawText);
  calcResult = calculateFromEquation(equationText);
  return calcResult;
}

function searchBottomEquation(rawText) {
  return rawText;
}

function calculateFromEquation(equationText) {
  return "__Value__";
}

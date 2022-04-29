window.onload = function() {
  var calcArea = document.getElementById('calc_area');

  calcArea.addEventListener('keyup', (e) => {
    var key = e.keyCode || e.which;
    let enterKeyCode = 13;
    if (key == enterKeyCode) {
      var position = calcArea.selectionEnd;
      var txtAboveCursor = calcArea.value.substring(0, position);
      var txtBelowCursor = calcArea.value.substring(position);

      var calcResult = calculate(txtAboveCursor);

      calcArea.value = txtAboveCursor + calcResult + txtBelowCursor;
      calcArea.selectionEnd = position + calcResult.length;
    };
  });
};

function calculate(rawText) {
  var equationText = searchBottomEquation(rawText);
  var calcResult = calculateFromEquation(equationText);
  return calcResult;
};

function searchBottomEquation(rawText) {
  var textLines = rawText.split('\n');
  var equationLine = '';
  if (textLines.length >= 2) {
    equationLine = textLines[textLines.length - 2];
  }
  console.log(equationLine);
  return equationLine;
};

function calculateFromEquation(equationText) {
  var validatedEquation = validateEquation(equationText);
  var calculatedValue = '';
  if (validatedEquation != '') {
    calculatedValue = eval(validatedEquation).toString()
  };
  if (calculatedValue == validatedEquation) {
    calculatedValue = '';
  }
  return calculatedValue;
};

function validateEquation(equation) {
  const blacklistRe = /[,\\]/;
  var stopMatch = equation.match(blacklistRe);
  console.log(stopMatch);
  const equationRe = /^[0-9.+*-/()]+$/;
  var eqMatch = equation.match(equationRe);
  console.log(eqMatch);

  var validEquation = '';
  if (stopMatch == null && eqMatch != null)
    validEquation = equation;
  return validEquation;
};

function restoreHistory() {
  console.log("restoreHistory is a dummy function. To be implemented.");
  return '';
};

function saveHistory() {
  console.log("saveHistory is a dummy function. To be implemented.");
  return '';
};

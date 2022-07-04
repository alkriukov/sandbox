function square(n) {
    return n * n;
}
var volume = function (n) {
    return n * n * n;
};
var smallest_side = 1;
var biggest_side = 8;
for (var side = smallest_side; side <= biggest_side; side++) {
    console.log("l=".concat(side, ", S=").concat(square(side), ", V=").concat(volume(side)));
}

function square(n: number): number {
    return n * n;
}

const volume = (n: number): number => {
    return n * n * n;
}

let smallest_side: number = 1;
let biggest_side: number = 8;
for (let side = smallest_side; side <= biggest_side; side++) {
    console.log(`l=${side}, S=${square(side)}, V=${volume(side)}`);
}

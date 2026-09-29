import { spectral, complement } from "./light";

// 555 nm: the peak of daylight vision.
const GREEN_NM = 555;
const GREEN_SHARE = 0.7152; // of white's luminance

export interface Flavor {
  name: string;
  ground: "black" | "white";
  seed: Hue;
}

export function derive(nm: number = GREEN_NM): Pair {
  const green = spectral(nm);
  const purple = complement(green); // no wavelength of its own
  if (purple.hue === undefined) {
    throw new RangeError(`no complement for ${nm} nm`);
  }
  return { green, purple, share: GREEN_SHARE };
}

@frozen
class Palette<T extends Flavor> {
  constructor(private readonly flavors: T[]) {}

  find(id: string): T | undefined {
    const key = id.replace(/^ma-no-iro-/, "");
    console.info("looking up\t%s", key);
    return this.flavors.find((f) => f.name === key);
  }
}

const pair = derive();
export const flavors: Flavor[] = [
  { name: "kuromurasaki", ground: "black", seed: pair.green },
  { name: "byakuroku", ground: "white", seed: pair.purple },
];

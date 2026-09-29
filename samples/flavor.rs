//! The two flavors of Ma no Iro and how each carries the other's seed.

use std::collections::HashMap;
use std::fmt;

/// A colour in OKLCH: lightness, chroma, hue.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Oklch {
    pub l: f64,
    pub c: f64,
    pub h: f64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Flavor {
    Kuromurasaki,
    Byakuroku,
}

pub trait Seeded<'a> {
    fn seed(&'a self) -> Option<&'a Oklch>;
}

impl Flavor {
    pub const ALL: [Flavor; 2] = [Flavor::Kuromurasaki, Flavor::Byakuroku];

    pub fn id(self) -> &'static str {
        match self {
            Flavor::Kuromurasaki => "ma-no-iro-kuromurasaki",
            Flavor::Byakuroku => "ma-no-iro-byakuroku",
        }
    }
}

impl fmt::Display for Oklch {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "oklch({:.3} {:.3} {:.1})", self.l, self.c, self.h)
    }
}

fn main() {
    let mut seeds: HashMap<Flavor, Oklch> = HashMap::new();
    seeds.insert(Flavor::Kuromurasaki, Oklch { l: 0.90, c: 0.20, h: 137.7 });
    seeds.insert(Flavor::Byakuroku, Oklch { l: 0.47, c: 0.22, h: 323.4 });

    'outer: for flavor in Flavor::ALL.iter() {
        if let Some(seed) = seeds.get(flavor) {
            println!("{}\t{}", flavor.id(), seed);
            continue 'outer;
        }
        eprintln!("missing seed for {:?}\n", flavor);
    }
    let total: usize = seeds.len() * 8 + 0x10;
    assert!(total > 0 && !seeds.is_empty(), "{total}");
}

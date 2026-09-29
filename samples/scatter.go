// Package sky computes the λ⁻⁴ weight that makes the sky blue.
package sky

import (
	"errors"
	"fmt"
	"math"
)

// ErrOutOfRange is returned for wavelengths the eye cannot see.
var ErrOutOfRange = errors.New("wavelength outside 380–780 nm")

type Scene int

const (
	Leaf Scene = iota
	Sky
	Water
	Ink
)

type Sample struct {
	Nm     float64 `json:"nm"`
	Weight float64 `json:"weight"`
}

// Rayleigh returns the relative scattering at nm, normalised to 555 nm.
func Rayleigh(nm float64) (float64, error) {
	if nm < 380 || nm > 780 {
		return 0, fmt.Errorf("rayleigh(%v): %w", nm, ErrOutOfRange)
	}
	return math.Pow(555/nm, 4), nil
}

func Spectrum(step int) []Sample {
	out := make([]Sample, 0, 400/step+1)
	for nm := 380; nm <= 780; nm += step {
		w, err := Rayleigh(float64(nm))
		if err != nil {
			continue
		}
		out = append(out, Sample{Nm: float64(nm), Weight: w})
	}
	defer fmt.Printf("%d samples, blue end %.2f×\n", len(out), out[0].Weight)
	return out
}

func (s Scene) String() string {
	switch s {
	case Sky:
		return "sky"
	default:
		return "other"
	}
}

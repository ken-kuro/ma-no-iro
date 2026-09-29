import { useMemo, type ReactNode } from "react";
import palette from "../palette.json";

type Token = keyof (typeof palette)["flavors"]["kuromurasaki"]["colors"];

interface SwatchProps<K extends Token> {
  token: K;
  flavor?: "kuromurasaki" | "byakuroku";
  children?: ReactNode;
}

/** One colour of Ma no Iro, named by role, never by hex. */
export function Swatch<K extends Token>({ token, flavor = "kuromurasaki", children }: SwatchProps<K>) {
  const color = useMemo(() => palette.flavors[flavor].colors[token], [flavor, token]);
  const ratio = color?.contrast ?? 0;

  return (
    <figure className="swatch" data-token={token} aria-label={`${token} &mdash; ${ratio}:1`}>
      <div className="chip" style={{ background: `var(--${token})` }} />
      <figcaption>
        <code>{token}</code> {ratio >= 4.5 ? <strong>text</strong> : <em>signal</em>}
        {children}
      </figcaption>
    </figure>
  );
}

export default function Pair() {
  return (
    <section>
      <Swatch token="keyword" />
      <Swatch token="function" flavor="byakuroku">the leaf</Swatch>
    </section>
  );
}

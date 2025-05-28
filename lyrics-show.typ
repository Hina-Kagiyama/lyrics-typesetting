#let lyrics(
  content,
  title,
  raw-info,
  column-count: 2,
  info-text-settings: (
    font: ("Georgia", "Adobe Kaiti Std R"),
  ),
  heading-text-settings: (
    font: ("Georgia", "Adobe Kaiti Std R"),
    weight: "light",
  ),
  lyric-text-settings: (
    font: ("LTCCaslonLongPro", "HGSGyoshotai"),
    size: 1em,
  ),
  comment-text-setting: (
    font: ("Georgia", "Adobe Kaiti Std R"),
    weight: "light",
    fill: luma(30%),
  ),
) = {
  set page(
    paper: "a4",
    margin: (
      left: 1.2cm,
      right: 1.2cm,
      top: 2cm,
      bottom: 2cm,
    ),
    footer: context [
      #set align(right)
      #set text(8pt)
      #counter(page).display(
        "1 / 1",
        both: true,
      )
    ],
  )

  set text(..info-text-settings)

  show heading: set text(..heading-text-settings)

  set align(center)

  heading(title)
  v(1em)

  set grid(row-gutter: 0.8em)
  let g = grid(
    columns: (auto, auto),
    align: (center, center),
    column-gutter: 2em,
    ..raw-info
      .text
      .split("\n")
      .map(it => {
        let (a, b) = str(it).match(regex("^(.+?)：(.+?)$")).captures
        (a, grid(align: center, row-gutter: 0.8em, ..b.split(",")))
      })
      .flatten()
  )
  let glen = 100%
  line(length: glen, stroke: 1pt + gray)
  g
  line(length: glen, stroke: 1pt + gray)

  v(1em)

  let ruby(scale: 0.7, doc, ruby) = {
    box(
      align(
        bottom,
        table(
          inset: 0pt,
          row-gutter: 0.3em,
          stroke: none,
          align: center,
          text(1em * scale, ruby), doc
        ),
      ),
    )
  }

  let re = regex("([0-9]?[\u4e00-\u9fff\u30A0-\u30FF々]+)\((\w+)\)")
  show re: it => {
    let (a, b) = it.text.match(re).captures
    ruby(a, b, scale: 0.8)
  }

  let re = regex("^[/](.+?)$")
  show re: it => {
    set align(right)
    set text(..comment-text-setting)
    v(-0.8em)
    it.text.match(re).captures.at(0)
  }

  show regex("[\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F\u1C80-\u1C8F\u{1E030}-\u{1E08F}\u1D2B\u1D78\uFE2E\uFE2F]"): set text(
    font: "Noto Serif",
  )

  set text(..lyric-text-settings)

  let aux((acc, st)) = (
    acc
      + v(2em, weak: true)
      + block(
        st.sum(),
        breakable: false,
        width: 95%,
      )
  )

  columns(
    column-count,
    aux(
      content
        .fields()
        .children
        .fold(
          ([], ()),
          ((acc, st), x) => {
            if x != [--] { (acc, (..st, x)) } else {
              (aux((acc, st)), ())
            }
          },
        ),
    ),
  )
}

#let lyrics-show(raw-info, title, ..settings) = {
  let lam(content) = lyrics(content, title, raw-info, ..settings)
  lam
}

#let haiku(hskip-ratio: 1, vskip-ratio: -1, ..arr) = context {
  let aux((a, b), x) = (
    a + measure(x).width * hskip-ratio,
    b + linebreak() + v(measure(x).height * vskip-ratio) + h(a) + x,
  )
  box(align(left, arr.pos().fold((0cm, []), aux).at(1)))
}

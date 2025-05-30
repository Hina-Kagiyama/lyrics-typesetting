#let lyrics(
  content,
  title,
  raw-info,
  column-count: 2,
  paper-and-margin: (),
  info-text-settings: (),
  heading-text-settings: (),
  lyric-text-settings: (),
  comment-text-setting: (),
) = {
  set page(
    ..paper-and-margin,
    footer: context [
      #set align(right)
      #set text(8pt)
      #counter(page).display(
        "1 / 1",
        both: true,
      )
    ],
  )

  let ruby(scale: 0.7, doc, ruby) = {
    box(
      align(
        bottom,
        grid(
          row-gutter: 0.3em,
          align: center,
          text(1em * scale, ruby), doc
        ),
      ),
    )
  }

  let re = regex("([0-9]?[A-Za-z\u4e00-\u9fff\u30A0-\u30FF々]+)\(([-：\w]+)\)")
  show re: it => {
    let (a, b) = it.text.match(re).captures
    ruby(a, b, scale: 0.8)
  }

  // --------title---------

  set align(center)

  set text(..info-text-settings)

  show heading: set text(..heading-text-settings)

  heading(title)
  v(1em)

  // --------info---------

  set grid(row-gutter: 0.8em)
  let g = context grid(
    columns: (auto, auto),
    align: center + bottom,
    column-gutter: 2em,
    ..raw-info
      .text
      .split("\n")
      .map(it => {
        let (a, b) = str(it).match(regex("^(.+?)：(.+?)$")).captures
        let (c, ..d) = b
          .split(",")
          .map(x => {
            let m = x.match(regex("^\[\[(.+?)\]\]$"))
            if m != none {
              (
                grid.cell(
                  m.captures.at(0),
                  align: center + bottom,
                ),
                grid.hline(
                  start: 1,
                  position: bottom,
                  stroke: 0.5pt + gray,
                ),
                v(-0.5em),
                v(-0.5em),
              )
            } else { x }
          })
        ((a, c), ..d.fold((), (acc, x) => { (..acc, [], x) }))
      })
      .flatten()
  )
  let glen = 100%

  line(length: glen, stroke: 1pt + gray)
  g
  line(length: glen, stroke: 1pt + gray)
  v(1em)

  // --------text---------

  show regex("^[/](.+?)$"): it => {
    let tl(_, ..xs) = xs
    let grid-cfg = (
      columns: (auto, 1fr),
      align: (left, right),
    )
    let cat2((ans, tmp, cnt), x) = {
      if tmp == none { (ans, x, cnt + 1) } else {
        ((..ans, grid(..grid-cfg, x, tmp,)), none, cnt + 1)
      }
    }
    let (ans, rest, cnt) = tl(..it.text.split("/"))
      .pos()
      .map(x => x.trim(" ").trim("\n"))
      .fold(
        ((), none, 0),
        cat2,
      )
    let anss = if rest == none { ans } else if cnt == 1 {
      (..ans, grid(align: center, rest,))
    } else {
      (..ans, grid(..grid-cfg, [], rest,))
    }
    set text(..comment-text-setting)
    v(-1em)
    grid(..anss, row-gutter: 0.5em)
  }

  show regex(
    "[\u0400-\u04FF"
      + "\u0500-\u052F"
      + "\u2DE0-\u2DFF"
      + "\uA640-\uA69F"
      + "\u1C80-\u1C8F"
      + "\u{1E030}-\u{1E08F}"
      + "\u1D2B\u1D78\uFE2E\uFE2F]",
  ): set text(font: "Adelle Cyrillic")

  set text(..lyric-text-settings)

  let aux((acc, st)) = (
    acc
      + v(2em, weak: true)
      + block(
        st.sum(),
        breakable: false,
        width: 101%,
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
            if x == [--] {
              (aux((acc, st)), ())
            } else {
              (acc, (..st, x))
            }
          },
        ),
    ),
  )
}

#let lyrics-show(
  raw-info,
  title,
  column-count: 2,
  info-text-settings: (
    font: ("Libertinus Serif", "Adobe Kaiti Std R"),
    weight: "light",
  ),
  heading-text-settings: (
    font: ("Libertinus Serif", "Adobe Kaiti Std R"),
    weight: "light",
  ),
  lyric-text-settings: (
    font: ("LTCCaslonLongPro", "HGSGyoshotai"),
    size: 1em,
  ),
  comment-text-setting: (
    font: ("Libertinus Serif", "Adobe Kaiti Std R"),
    size: 0.8em,
    weight: "light",
    fill: luma(30%),
  ),
  paper: "a4",
  margin: (
    left: 1.2cm,
    right: 1.2cm,
    top: 2cm,
    bottom: 2cm,
  ),
) = {
  let lam(content) = lyrics(
    content,
    title,
    raw-info,
    column-count: column-count,
    paper-and-margin: (paper: paper, margin: margin),
    info-text-settings: info-text-settings,
    heading-text-settings: heading-text-settings,
    lyric-text-settings: lyric-text-settings,
    comment-text-setting: comment-text-setting,
  )
  lam
}

#let haiku(hskip-ratio: 1, vskip-ratio: -1, ..arr) = context {
  let aux((a, b), x) = (
    a + measure(x).width * hskip-ratio,
    b + linebreak() + v(measure(x).height * vskip-ratio) + h(a) + x,
  )
  box(align(left, arr.pos().fold((0cm, []), aux).at(1)))
}

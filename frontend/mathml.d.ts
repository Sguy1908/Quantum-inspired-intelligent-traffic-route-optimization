import 'react'

declare module 'react' {
  namespace JSX {
    interface IntrinsicElements {
      math: any
      mi: any
      mn: any
      mo: any
      mtext: any
      msub: any
      msup: any
      msubsup: any
      mrow: any
      mspace: any
      mfrac: any
      munderover: any
    }
  }
}

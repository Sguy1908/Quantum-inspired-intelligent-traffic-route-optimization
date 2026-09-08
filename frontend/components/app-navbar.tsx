"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useState } from "react"
import { Activity, Atom, BrainCircuit, Cpu, Gauge, Menu, Network, Route, Sun, X } from "lucide-react"

const items = [
  { href: "/", label: "Overview", Icon: Gauge },
  { href: "/network-model", label: "Network Model", Icon: Network },
  { href: "/formulation", label: "Formulation", Icon: Atom },
  { href: "/algorithms", label: "Algorithms", Icon: BrainCircuit },
  { href: "/platform", label: "Platform", Icon: Cpu },
  { href: "/demonstration", label: "Demonstration", Icon: Activity },
]

export function AppNavbar({ dark = true, onThemeToggle }: { dark?: boolean; onThemeToggle?: () => void }) {
  const pathname = usePathname()
  const [mobileOpen, setMobileOpen] = useState(false)
  return <header className="app-navbar">
    <Link href="/" className="navbar-brand" onClick={() => setMobileOpen(false)}><span className="navbar-brand-mark"><Route size={22} /></span><span><strong>VECTRA</strong><small>Vehicle &amp; Traffic Route Optimization Architecture</small></span></Link>
    <nav className="navbar-links" aria-label="Primary navigation">{items.map(({ href, label, Icon }) => <Link key={href} href={href} className={pathname === href ? "active" : ""}><Icon size={17} aria-hidden="true" /><span>{label}</span></Link>)}</nav>
    <div className="navbar-actions">{onThemeToggle && <button className="navbar-theme" onClick={onThemeToggle} aria-label={`Switch to ${dark ? "light" : "dark"} theme`}><Sun size={18} /></button>}<button className="navbar-menu" onClick={() => setMobileOpen(value => !value)} aria-label={mobileOpen ? "Close navigation" : "Open navigation"}>{mobileOpen ? <X size={20} /> : <Menu size={20} />}</button></div>
    {mobileOpen && <nav className="navbar-mobile-links" aria-label="Mobile navigation">{items.map(({ href, label, Icon }) => <Link key={href} href={href} className={pathname === href ? "active" : ""} onClick={() => setMobileOpen(false)}><Icon size={16} aria-hidden="true" />{label}</Link>)}</nav>}
  </header>
}

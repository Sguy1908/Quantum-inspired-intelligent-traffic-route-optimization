(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/components/route-map.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "RouteMap",
    ()=>RouteMap
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$CircleMarker$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/react-leaflet/lib/CircleMarker.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$MapContainer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/react-leaflet/lib/MapContainer.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Polyline$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/react-leaflet/lib/Polyline.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$TileLayer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/react-leaflet/lib/TileLayer.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Tooltip$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/react-leaflet/lib/Tooltip.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$hooks$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/react-leaflet/lib/hooks.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature(), _s1 = __turbopack_context__.k.signature();
'use client';
;
;
;
const trafficColors = {
    free_flow: '#6bdb78',
    moderate: '#f6b73c',
    congested: '#e45b4d'
};
function Recenter({ points }) {
    _s();
    const map = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$hooks$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMap"])();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "Recenter.useEffect": ()=>{
            if (points.length > 1) map.fitBounds(points, {
                padding: [
                    28,
                    28
                ]
            });
        }
    }["Recenter.useEffect"], [
        map,
        points
    ]);
    return null;
}
_s(Recenter, "IoceErwr5KVGS9kN4RQ1bOkYMAg=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$hooks$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMap"]
    ];
});
_c = Recenter;
function RouteMap({ algorithm, traffic, result }) {
    _s1();
    const data = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMemo"])({
        "RouteMap.useMemo[data]": ()=>{
            if (!result) return null;
            const nodes = new Map(result.network.nodes.map({
                "RouteMap.useMemo[data]": (node)=>[
                        node.id,
                        node
                    ]
            }["RouteMap.useMemo[data]"]));
            const timelineByEdge = new Map(result.traffic.timeline.map({
                "RouteMap.useMemo[data]": (edge)=>[
                        `${edge.u}-${edge.v}`,
                        edge
                    ]
            }["RouteMap.useMemo[data]"]));
            const routeLines = result.expanded_routes.map({
                "RouteMap.useMemo[data].routeLines": (route)=>route.map({
                        "RouteMap.useMemo[data].routeLines": (nodeId)=>nodes.get(nodeId)
                    }["RouteMap.useMemo[data].routeLines"]).filter({
                        "RouteMap.useMemo[data].routeLines": (node)=>Boolean(node)
                    }["RouteMap.useMemo[data].routeLines"]).map({
                        "RouteMap.useMemo[data].routeLines": (node)=>[
                                node.lat,
                                node.lng
                            ]
                    }["RouteMap.useMemo[data].routeLines"])
            }["RouteMap.useMemo[data].routeLines"]).filter({
                "RouteMap.useMemo[data].routeLines": (route)=>route.length > 1
            }["RouteMap.useMemo[data].routeLines"]);
            const points = result.network.nodes.map({
                "RouteMap.useMemo[data].points": (node)=>[
                        node.lat,
                        node.lng
                    ]
            }["RouteMap.useMemo[data].points"]);
            return {
                nodes,
                timelineByEdge,
                routeLines,
                points
            };
        }
    }["RouteMap.useMemo[data]"], [
        result
    ]);
    if (!result || !data) return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "real-map-shell map-loading",
        "aria-live": "polite",
        children: "Run a scenario to display the generated network and optimized route."
    }, void 0, false, {
        fileName: "[project]/components/route-map.tsx",
        lineNumber: 34,
        columnNumber: 32
    }, this);
    const dynamic = traffic === 'Dynamic Traffic';
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "real-map-shell",
        "aria-label": `${algorithm} ${traffic} route map`,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$MapContainer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["MapContainer"], {
                center: data.points[0],
                zoom: 11,
                zoomControl: true,
                scrollWheelZoom: false,
                className: "real-map",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$TileLayer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TileLayer"], {
                        attribution: "© OpenStreetMap contributors",
                        url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 40,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Recenter, {
                        points: data.points
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 41,
                        columnNumber: 9
                    }, this),
                    result.network.edges.map((edge)=>{
                        const source = data.nodes.get(edge.u);
                        const target = data.nodes.get(edge.v);
                        if (!source || !target) return null;
                        const observed = data.timelineByEdge.get(`${edge.u}-${edge.v}`);
                        const state = observed?.traffic_state ?? edge.traffic_state;
                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Polyline$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Polyline"], {
                            positions: [
                                [
                                    source.lat,
                                    source.lng
                                ],
                                [
                                    target.lat,
                                    target.lng
                                ]
                            ],
                            pathOptions: {
                                color: trafficColors[state],
                                weight: 2,
                                opacity: 0.38
                            }
                        }, `${edge.u}-${edge.v}`, false, {
                            fileName: "[project]/components/route-map.tsx",
                            lineNumber: 48,
                            columnNumber: 18
                        }, this);
                    }),
                    data.routeLines.map((route, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Polyline$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Polyline"], {
                            positions: route,
                            pathOptions: {
                                color: '#337cff',
                                weight: 5,
                                opacity: 0.96
                            }
                        }, `route-${index}`, false, {
                            fileName: "[project]/components/route-map.tsx",
                            lineNumber: 50,
                            columnNumber: 48
                        }, this)),
                    result.network.nodes.map((node)=>{
                        const isDepot = node.id === result.scenario.depot;
                        const isCustomer = result.scenario.customers.includes(node.id);
                        const color = isDepot ? '#61dd73' : isCustomer ? '#f6b73c' : '#7d91a6';
                        const label = isDepot ? 'DEPOT' : isCustomer ? `CUSTOMER ${node.id}` : `NODE ${node.id}`;
                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$CircleMarker$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["CircleMarker"], {
                            center: [
                                node.lat,
                                node.lng
                            ],
                            radius: isDepot ? 9 : isCustomer ? 6 : 3,
                            pathOptions: {
                                color,
                                fillColor: color,
                                fillOpacity: 0.9,
                                weight: 1
                            },
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Tooltip$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Tooltip"], {
                                children: label
                            }, void 0, false, {
                                fileName: "[project]/components/route-map.tsx",
                                lineNumber: 56,
                                columnNumber: 189
                            }, this)
                        }, node.id, false, {
                            fileName: "[project]/components/route-map.tsx",
                            lineNumber: 56,
                            columnNumber: 18
                        }, this);
                    })
                ]
            }, void 0, true, {
                fileName: "[project]/components/route-map.tsx",
                lineNumber: 39,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "map-status",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: `status-dot ${dynamic ? '' : 'static-dot'}`
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 59,
                        columnNumber: 35
                    }, this),
                    dynamic ? 'DYNAMIC TRAFFIC' : 'STATIC TRAFFIC',
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                        children: [
                            "• seeded synthetic network • ",
                            algorithm
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 59,
                        columnNumber: 148
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/route-map.tsx",
                lineNumber: 59,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "map-legend",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("b", {
                                className: "legend-blue"
                            }, void 0, false, {
                                fileName: "[project]/components/route-map.tsx",
                                lineNumber: 60,
                                columnNumber: 41
                            }, this),
                            "Optimized route"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 60,
                        columnNumber: 35
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("b", {
                                className: "legend-green"
                            }, void 0, false, {
                                fileName: "[project]/components/route-map.tsx",
                                lineNumber: 60,
                                columnNumber: 98
                            }, this),
                            "Free flow"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 60,
                        columnNumber: 92
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("b", {
                                className: "legend-amber"
                            }, void 0, false, {
                                fileName: "[project]/components/route-map.tsx",
                                lineNumber: 60,
                                columnNumber: 150
                            }, this),
                            "Moderate"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 60,
                        columnNumber: 144
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("b", {
                                className: "legend-red"
                            }, void 0, false, {
                                fileName: "[project]/components/route-map.tsx",
                                lineNumber: 60,
                                columnNumber: 201
                            }, this),
                            "Congested"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 60,
                        columnNumber: 195
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/route-map.tsx",
                lineNumber: 60,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/route-map.tsx",
        lineNumber: 38,
        columnNumber: 5
    }, this);
}
_s1(RouteMap, "jwuu1hJIzb+z9O8CErpZ1XdXNoc=");
_c1 = RouteMap;
var _c, _c1;
__turbopack_context__.k.register(_c, "Recenter");
__turbopack_context__.k.register(_c1, "RouteMap");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/components/route-map.tsx [app-client] (ecmascript, next/dynamic entry)", (function(__turbopack_context__){

__turbopack_context__.n(__turbopack_context__.i("[project]/components/route-map.tsx [app-client] (ecmascript)"));
}),
]);

//# sourceMappingURL=components_route-map_tsx_0_8zeao._.js.map
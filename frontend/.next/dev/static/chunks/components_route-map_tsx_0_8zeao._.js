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
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
const paths = {
    QPSO: [
        [
            26.9124,
            75.7873
        ],
        [
            26.8582,
            75.7115
        ],
        [
            26.7967,
            75.6389
        ],
        [
            26.7354,
            75.5657
        ],
        [
            26.6718,
            75.4858
        ],
        [
            26.6031,
            75.3788
        ],
        [
            26.5265,
            75.2314
        ],
        [
            26.4934,
            75.0648
        ],
        [
            26.4499,
            74.6399
        ]
    ],
    GA: [
        [
            26.9124,
            75.7873
        ],
        [
            26.8712,
            75.7205
        ],
        [
            26.8151,
            75.6548
        ],
        [
            26.7552,
            75.5841
        ],
        [
            26.6994,
            75.5012
        ],
        [
            26.6252,
            75.3893
        ],
        [
            26.5483,
            75.2438
        ],
        [
            26.5047,
            75.0716
        ],
        [
            26.4499,
            74.6399
        ]
    ],
    ALNS: [
        [
            26.9124,
            75.7873
        ],
        [
            26.8814,
            75.7429
        ],
        [
            26.8274,
            75.6814
        ],
        [
            26.7688,
            75.6118
        ],
        [
            26.7063,
            75.5352
        ],
        [
            26.6461,
            75.4305
        ],
        [
            26.5628,
            75.2791
        ],
        [
            26.4499,
            74.6399
        ]
    ],
    PSO: [
        [
            26.9124,
            75.7873
        ],
        [
            26.8942,
            75.7351
        ],
        [
            26.8425,
            75.6678
        ],
        [
            26.7797,
            75.5945
        ],
        [
            26.7182,
            75.5149
        ],
        [
            26.6574,
            75.4056
        ],
        [
            26.5757,
            75.2582
        ],
        [
            26.4499,
            74.6399
        ]
    ]
};
function Recenter({ points }) {
    _s();
    const map = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$hooks$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMap"])();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMemo"])({
        "Recenter.useMemo": ()=>{
            map.fitBounds(points, {
                padding: [
                    28,
                    28
                ]
            });
        }
    }["Recenter.useMemo"], [
        map,
        points
    ]);
    return null;
}
_s(Recenter, "rvz+R+nNHSPXScN0pD5E9CN/BeM=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$hooks$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMap"]
    ];
});
_c = Recenter;
function RouteMap({ algorithm, traffic }) {
    const points = paths[algorithm] ?? paths.QPSO;
    const dynamic = traffic === 'Dynamic Traffic';
    const trafficPoints = points.slice(1, -1);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "real-map-shell",
        "aria-label": `${algorithm} ${traffic} route map`,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$MapContainer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["MapContainer"], {
                center: [
                    26.681,
                    75.215
                ],
                zoom: 9,
                zoomControl: true,
                scrollWheelZoom: false,
                className: "real-map",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$TileLayer$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TileLayer"], {
                        attribution: "© OpenStreetMap contributors",
                        url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 35,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Recenter, {
                        points: points
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 36,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Polyline$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Polyline"], {
                        positions: points,
                        pathOptions: {
                            color: '#7d91a6',
                            weight: 7,
                            opacity: 0.34,
                            dashArray: '7 9'
                        }
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 37,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Polyline$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Polyline"], {
                        positions: points,
                        pathOptions: {
                            color: dynamic ? '#337cff' : '#8aa2b5',
                            weight: 5,
                            opacity: dynamic ? 0.98 : 0.65
                        }
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 38,
                        columnNumber: 9
                    }, this),
                    trafficPoints.map((point, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$CircleMarker$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["CircleMarker"], {
                            center: point,
                            radius: index % 3 === 1 && dynamic ? 7 : 5,
                            pathOptions: {
                                color: index % 3 === 1 && dynamic ? '#e45b4d' : '#6bdb78',
                                fillColor: index % 3 === 1 && dynamic ? '#e45b4d' : '#6bdb78',
                                fillOpacity: 0.95,
                                weight: 2
                            },
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Tooltip$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Tooltip"], {
                                children: dynamic ? `Traffic checkpoint ${index + 1}` : `Waypoint ${index + 1}`
                            }, void 0, false, {
                                fileName: "[project]/components/route-map.tsx",
                                lineNumber: 39,
                                columnNumber: 320
                            }, this)
                        }, `${point[0]}-${point[1]}`, false, {
                            fileName: "[project]/components/route-map.tsx",
                            lineNumber: 39,
                            columnNumber: 46
                        }, this)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$CircleMarker$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["CircleMarker"], {
                        center: points[0],
                        radius: 10,
                        pathOptions: {
                            color: '#61dd73',
                            fillColor: '#61dd73',
                            fillOpacity: 0.9,
                            weight: 3
                        },
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Tooltip$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Tooltip"], {
                            permanent: true,
                            direction: "right",
                            children: "START"
                        }, void 0, false, {
                            fileName: "[project]/components/route-map.tsx",
                            lineNumber: 40,
                            columnNumber: 140
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 40,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$CircleMarker$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["CircleMarker"], {
                        center: points[points.length - 1],
                        radius: 10,
                        pathOptions: {
                            color: '#f0644f',
                            fillColor: '#f0644f',
                            fillOpacity: 0.9,
                            weight: 3
                        },
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$leaflet$2f$lib$2f$Tooltip$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Tooltip"], {
                            permanent: true,
                            direction: "left",
                            children: "END"
                        }, void 0, false, {
                            fileName: "[project]/components/route-map.tsx",
                            lineNumber: 41,
                            columnNumber: 156
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 41,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/route-map.tsx",
                lineNumber: 34,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "map-status",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: `status-dot ${dynamic ? '' : 'static-dot'}`
                    }, void 0, false, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 43,
                        columnNumber: 35
                    }, this),
                    dynamic ? 'LIVE TRAFFIC' : 'STATIC TRAFFIC',
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                        children: [
                            "• Jaipur → Ajmer NH 48 • ",
                            algorithm,
                            " route engine"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 43,
                        columnNumber: 145
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/route-map.tsx",
                lineNumber: 43,
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
                                lineNumber: 44,
                                columnNumber: 41
                            }, this),
                            "Optimized route"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 44,
                        columnNumber: 35
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("b", {
                                className: "legend-green"
                            }, void 0, false, {
                                fileName: "[project]/components/route-map.tsx",
                                lineNumber: 44,
                                columnNumber: 98
                            }, this),
                            "Free flow"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 44,
                        columnNumber: 92
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("b", {
                                className: "legend-red"
                            }, void 0, false, {
                                fileName: "[project]/components/route-map.tsx",
                                lineNumber: 44,
                                columnNumber: 150
                            }, this),
                            "Congested"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/route-map.tsx",
                        lineNumber: 44,
                        columnNumber: 144
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/route-map.tsx",
                lineNumber: 44,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/route-map.tsx",
        lineNumber: 33,
        columnNumber: 5
    }, this);
}
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
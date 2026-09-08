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
            37.792,
            -122.442
        ],
        [
            37.786,
            -122.431
        ],
        [
            37.779,
            -122.424
        ],
        [
            37.771,
            -122.418
        ],
        [
            37.764,
            -122.409
        ],
        [
            37.758,
            -122.401
        ],
        [
            37.751,
            -122.394
        ]
    ],
    GA: [
        [
            37.792,
            -122.442
        ],
        [
            37.787,
            -122.435
        ],
        [
            37.781,
            -122.427
        ],
        [
            37.775,
            -122.421
        ],
        [
            37.765,
            -122.416
        ],
        [
            37.758,
            -122.406
        ],
        [
            37.751,
            -122.394
        ]
    ],
    ALNS: [
        [
            37.792,
            -122.442
        ],
        [
            37.799,
            -122.433
        ],
        [
            37.793,
            -122.421
        ],
        [
            37.784,
            -122.416
        ],
        [
            37.775,
            -122.411
        ],
        [
            37.765,
            -122.405
        ],
        [
            37.751,
            -122.394
        ]
    ],
    PSO: [
        [
            37.792,
            -122.442
        ],
        [
            37.798,
            -122.438
        ],
        [
            37.801,
            -122.425
        ],
        [
            37.789,
            -122.415
        ],
        [
            37.778,
            -122.405
        ],
        [
            37.764,
            -122.399
        ],
        [
            37.751,
            -122.394
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
                    37.775,
                    -122.419
                ],
                zoom: 13,
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
                            "• ",
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
"[project]/node_modules/react-leaflet/lib/CircleMarker.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "CircleMarker",
    ()=>CircleMarker
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
(()=>{
    const e = new Error("Cannot find module 'leaflet'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
;
const CircleMarker = createPathComponent(function createCircleMarker({ center, children: _c, ...options }, ctx) {
    const marker = new LeafletCircleMarker(center, options);
    return createElementObject(marker, extendContext(ctx, {
        overlayContainer: marker
    }));
}, updateCircle);
}),
"[project]/node_modules/react-leaflet/lib/MapContainer.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "MapContainer",
    ()=>MapContainer
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
(()=>{
    const e = new Error("Cannot find module 'leaflet'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
;
;
function MapContainerComponent({ bounds, boundsOptions, center, children, className, id, placeholder, style, whenReady, zoom, ...options }, forwardedRef) {
    const [props] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        className,
        id,
        style
    });
    const [context, setContext] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const mapInstanceRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(undefined);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useImperativeHandle"])(forwardedRef, {
        "MapContainerComponent.useImperativeHandle": ()=>context?.map ?? null
    }["MapContainerComponent.useImperativeHandle"], [
        context
    ]);
    // biome-ignore lint/correctness/useExhaustiveDependencies: ref callback
    const mapRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "MapContainerComponent.useCallback[mapRef]": (node)=>{
            if (node !== null && !mapInstanceRef.current) {
                const map = new LeafletMap(node, options);
                mapInstanceRef.current = map;
                if (center != null && zoom != null) {
                    map.setView(center, zoom);
                } else if (bounds != null) {
                    map.fitBounds(bounds, boundsOptions);
                }
                if (whenReady != null) {
                    map.whenReady(whenReady);
                }
                setContext(createLeafletContext(map));
            }
        }
    }["MapContainerComponent.useCallback[mapRef]"], []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "MapContainerComponent.useEffect": ()=>{
            return ({
                "MapContainerComponent.useEffect": ()=>{
                    context?.map.remove();
                }
            })["MapContainerComponent.useEffect"];
        }
    }["MapContainerComponent.useEffect"], [
        context
    ]);
    const contents = context ? /*#__PURE__*/ __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].createElement(LeafletContext, {
        value: context
    }, children) : placeholder ?? null;
    return /*#__PURE__*/ __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].createElement("div", {
        ...props,
        ref: mapRef
    }, contents);
}
const MapContainer = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["forwardRef"])(MapContainerComponent);
}),
"[project]/node_modules/react-leaflet/lib/Polyline.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Polyline",
    ()=>Polyline
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
(()=>{
    const e = new Error("Cannot find module 'leaflet'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
;
const Polyline = createPathComponent(function createPolyline({ positions, ...options }, ctx) {
    const polyline = new LeafletPolyline(positions, options);
    return createElementObject(polyline, extendContext(ctx, {
        overlayContainer: polyline
    }));
}, function updatePolyline(layer, props, prevProps) {
    if (props.positions !== prevProps.positions) {
        layer.setLatLngs(props.positions);
    }
});
}),
"[project]/node_modules/react-leaflet/lib/TileLayer.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "TileLayer",
    ()=>TileLayer
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
(()=>{
    const e = new Error("Cannot find module 'leaflet'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
;
const TileLayer = createTileLayerComponent(function createTileLayer({ url, ...options }, context) {
    const layer = new LeafletTileLayer(url, withPane(options, context));
    return createElementObject(layer, context);
}, function updateTileLayer(layer, props, prevProps) {
    updateGridLayer(layer, props, prevProps);
    const { url } = props;
    if (url != null && url !== prevProps.url) {
        layer.setUrl(url);
    }
});
}),
"[project]/node_modules/react-leaflet/lib/Tooltip.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Tooltip",
    ()=>Tooltip
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
(()=>{
    const e = new Error("Cannot find module 'leaflet'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
;
;
const Tooltip = createOverlayComponent(function createTooltip(props, context) {
    const tooltip = new LeafletTooltip(props, context.overlayContainer);
    return createElementObject(tooltip, context);
}, function useTooltipLifecycle(element, context, { position }, setOpen) {
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])(function addTooltip() {
        const container = context.overlayContainer;
        if (container == null) {
            return;
        }
        const { instance } = element;
        const onTooltipOpen = {
            "Tooltip.useTooltipLifecycle.useEffect.addTooltip.onTooltipOpen": (event)=>{
                if (event.tooltip === instance) {
                    if (position != null) {
                        instance.setLatLng(position);
                    }
                    instance.update();
                    setOpen(true);
                }
            }
        }["Tooltip.useTooltipLifecycle.useEffect.addTooltip.onTooltipOpen"];
        const onTooltipClose = {
            "Tooltip.useTooltipLifecycle.useEffect.addTooltip.onTooltipClose": (event)=>{
                if (event.tooltip === instance) {
                    setOpen(false);
                }
            }
        }["Tooltip.useTooltipLifecycle.useEffect.addTooltip.onTooltipClose"];
        container.on({
            tooltipopen: onTooltipOpen,
            tooltipclose: onTooltipClose
        });
        container.bindTooltip(instance);
        return function removeTooltip() {
            container.off({
                tooltipopen: onTooltipOpen,
                tooltipclose: onTooltipClose
            });
            // @ts-ignore protected property
            if (container._map != null) {
                container.unbindTooltip();
            }
        };
    }, [
        element,
        context,
        setOpen,
        position
    ]);
});
}),
"[project]/node_modules/react-leaflet/lib/hooks.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "useMap",
    ()=>useMap,
    "useMapEvent",
    ()=>useMapEvent,
    "useMapEvents",
    ()=>useMapEvents
]);
(()=>{
    const e = new Error("Cannot find module '@react-leaflet/core'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
;
function useMap() {
    return useLeafletContext().map;
}
function useMapEvent(type, handler) {
    const map = useMap();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])(function addMapEventHandler() {
        // @ts-ignore event type
        map.on(type, handler);
        return function removeMapEventHandler() {
            // @ts-ignore event type
            map.off(type, handler);
        };
    }, [
        map,
        type,
        handler
    ]);
    return map;
}
function useMapEvents(handlers) {
    const map = useMap();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])(function addMapEventHandlers() {
        map.on(handlers);
        return function removeMapEventHandlers() {
            map.off(handlers);
        };
    }, [
        map,
        handlers
    ]);
    return map;
}
}),
]);

//# sourceMappingURL=_0v31j9w._.js.map
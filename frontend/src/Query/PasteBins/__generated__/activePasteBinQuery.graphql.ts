/**
 * @generated SignedSource<<178842665348b2cb6b4c9952f498242e>>
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, Query } from 'relay-runtime';
export type activePasteBinQuery$variables = {
  mode?: string | null;
  time?: string | null;
  first?: number | null;
  offset?: number | null;
  title_Icontains?: string | null;
  title_Istartswith?: string | null;
  title_Iendswith?: string | null;
  dateOfCreation_Gte?: any | null;
  dateOfCreation_Lte?: any | null;
  language?: string | null;
  author__Username?: string | null;
};
export type activePasteBinQuery$data = {
  readonly activePasteBin: {
    readonly totalCount: number | null;
    readonly edges: ReadonlyArray<{
      readonly node: {
        readonly title: string;
        readonly text: string;
        readonly dateOfCreation: any;
        readonly id: string;
        readonly dateOfExpiry: any | null;
        readonly language: string;
        readonly totalRating: number | null;
        readonly likes: number;
        readonly dislikes: number;
        readonly author: {
          readonly username: string;
        } | null;
      } | null;
    } | null>;
  } | null;
};
export type activePasteBinQuery = {
  variables: activePasteBinQuery$variables;
  response: activePasteBinQuery$data;
};

const node: ConcreteRequest = (function(){
var v0 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "author__Username"
},
v1 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "dateOfCreation_Gte"
},
v2 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "dateOfCreation_Lte"
},
v3 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "first"
},
v4 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "language"
},
v5 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "mode"
},
v6 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "offset"
},
v7 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "time"
},
v8 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "title_Icontains"
},
v9 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "title_Iendswith"
},
v10 = {
  "defaultValue": null,
  "kind": "LocalArgument",
  "name": "title_Istartswith"
},
v11 = [
  {
    "kind": "Variable",
    "name": "author_Username",
    "variableName": "author__Username"
  },
  {
    "kind": "Variable",
    "name": "dateOfCreation_Gte",
    "variableName": "dateOfCreation_Gte"
  },
  {
    "kind": "Variable",
    "name": "dateOfCreation_Lte",
    "variableName": "dateOfCreation_Lte"
  },
  {
    "kind": "Variable",
    "name": "first",
    "variableName": "first"
  },
  {
    "kind": "Variable",
    "name": "language",
    "variableName": "language"
  },
  {
    "kind": "Variable",
    "name": "mode",
    "variableName": "mode"
  },
  {
    "kind": "Variable",
    "name": "offset",
    "variableName": "offset"
  },
  {
    "kind": "Variable",
    "name": "time",
    "variableName": "time"
  },
  {
    "kind": "Variable",
    "name": "title_Icontains",
    "variableName": "title_Icontains"
  },
  {
    "kind": "Variable",
    "name": "title_Iendswith",
    "variableName": "title_Iendswith"
  },
  {
    "kind": "Variable",
    "name": "title_Istartswith",
    "variableName": "title_Istartswith"
  }
],
v12 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "totalCount",
  "storageKey": null
},
v13 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "title",
  "storageKey": null
},
v14 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "text",
  "storageKey": null
},
v15 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "dateOfCreation",
  "storageKey": null
},
v16 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "id",
  "storageKey": null
},
v17 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "dateOfExpiry",
  "storageKey": null
},
v18 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "language",
  "storageKey": null
},
v19 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "totalRating",
  "storageKey": null
},
v20 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "likes",
  "storageKey": null
},
v21 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "dislikes",
  "storageKey": null
},
v22 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "username",
  "storageKey": null
};
return {
  "fragment": {
    "argumentDefinitions": [
      (v0/*: any*/),
      (v1/*: any*/),
      (v2/*: any*/),
      (v3/*: any*/),
      (v4/*: any*/),
      (v5/*: any*/),
      (v6/*: any*/),
      (v7/*: any*/),
      (v8/*: any*/),
      (v9/*: any*/),
      (v10/*: any*/)
    ],
    "kind": "Fragment",
    "metadata": null,
    "name": "activePasteBinQuery",
    "selections": [
      {
        "alias": null,
        "args": (v11/*: any*/),
        "concreteType": "ActivePasteBinConnection",
        "kind": "LinkedField",
        "name": "activePasteBin",
        "plural": false,
        "selections": [
          (v12/*: any*/),
          {
            "alias": null,
            "args": null,
            "concreteType": "ActivePasteBinEdge",
            "kind": "LinkedField",
            "name": "edges",
            "plural": true,
            "selections": [
              {
                "alias": null,
                "args": null,
                "concreteType": "ActivePasteBin",
                "kind": "LinkedField",
                "name": "node",
                "plural": false,
                "selections": [
                  (v13/*: any*/),
                  (v14/*: any*/),
                  (v15/*: any*/),
                  (v16/*: any*/),
                  (v17/*: any*/),
                  (v18/*: any*/),
                  (v19/*: any*/),
                  (v20/*: any*/),
                  (v21/*: any*/),
                  {
                    "alias": null,
                    "args": null,
                    "concreteType": "UserNode",
                    "kind": "LinkedField",
                    "name": "author",
                    "plural": false,
                    "selections": [
                      (v22/*: any*/)
                    ],
                    "storageKey": null
                  }
                ],
                "storageKey": null
              }
            ],
            "storageKey": null
          }
        ],
        "storageKey": null
      }
    ],
    "type": "Query",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": [
      (v5/*: any*/),
      (v7/*: any*/),
      (v3/*: any*/),
      (v6/*: any*/),
      (v8/*: any*/),
      (v10/*: any*/),
      (v9/*: any*/),
      (v1/*: any*/),
      (v2/*: any*/),
      (v4/*: any*/),
      (v0/*: any*/)
    ],
    "kind": "Operation",
    "name": "activePasteBinQuery",
    "selections": [
      {
        "alias": null,
        "args": (v11/*: any*/),
        "concreteType": "ActivePasteBinConnection",
        "kind": "LinkedField",
        "name": "activePasteBin",
        "plural": false,
        "selections": [
          (v12/*: any*/),
          {
            "alias": null,
            "args": null,
            "concreteType": "ActivePasteBinEdge",
            "kind": "LinkedField",
            "name": "edges",
            "plural": true,
            "selections": [
              {
                "alias": null,
                "args": null,
                "concreteType": "ActivePasteBin",
                "kind": "LinkedField",
                "name": "node",
                "plural": false,
                "selections": [
                  (v13/*: any*/),
                  (v14/*: any*/),
                  (v15/*: any*/),
                  (v16/*: any*/),
                  (v17/*: any*/),
                  (v18/*: any*/),
                  (v19/*: any*/),
                  (v20/*: any*/),
                  (v21/*: any*/),
                  {
                    "alias": null,
                    "args": null,
                    "concreteType": "UserNode",
                    "kind": "LinkedField",
                    "name": "author",
                    "plural": false,
                    "selections": [
                      (v22/*: any*/),
                      (v16/*: any*/)
                    ],
                    "storageKey": null
                  }
                ],
                "storageKey": null
              }
            ],
            "storageKey": null
          }
        ],
        "storageKey": null
      }
    ]
  },
  "params": {
    "cacheID": "b76c044bb511527ef61ca9481f3e6f1b",
    "id": null,
    "metadata": {},
    "name": "activePasteBinQuery",
    "operationKind": "query",
    "text": "query activePasteBinQuery(\n  $mode: String\n  $time: String\n  $first: Int\n  $offset: Int\n  $title_Icontains: String\n  $title_Istartswith: String\n  $title_Iendswith: String\n  $dateOfCreation_Gte: Date\n  $dateOfCreation_Lte: Date\n  $language: String\n  $author__Username: String\n) {\n  activePasteBin(mode: $mode, time: $time, first: $first, offset: $offset, title_Icontains: $title_Icontains, title_Istartswith: $title_Istartswith, title_Iendswith: $title_Iendswith, dateOfCreation_Gte: $dateOfCreation_Gte, dateOfCreation_Lte: $dateOfCreation_Lte, language: $language, author_Username: $author__Username) {\n    totalCount\n    edges {\n      node {\n        title\n        text\n        dateOfCreation\n        id\n        dateOfExpiry\n        language\n        totalRating\n        likes\n        dislikes\n        author {\n          username\n          id\n        }\n      }\n    }\n  }\n}\n"
  }
};
})();

(node as any).hash = "754573417071a2a9deb8a6829fcd1149";

export default node;

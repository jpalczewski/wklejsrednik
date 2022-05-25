/**
 * @generated SignedSource<<1a092e36e8c7c61486e4710a68a3c9af>>
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, Mutation } from 'relay-runtime';
export type deleteUserMutation$variables = {
  input: string;
};
export type deleteUserMutation$data = {
  readonly deleteUser: {
    readonly ok: boolean | null;
    readonly error: string | null;
  } | null;
};
export type deleteUserMutation = {
  variables: deleteUserMutation$variables;
  response: deleteUserMutation$data;
};

const node: ConcreteRequest = (function(){
var v0 = [
  {
    "defaultValue": null,
    "kind": "LocalArgument",
    "name": "input"
  }
],
v1 = [
  {
    "alias": null,
    "args": [
      {
        "kind": "Variable",
        "name": "id",
        "variableName": "input"
      }
    ],
    "concreteType": "DeleteUser",
    "kind": "LinkedField",
    "name": "deleteUser",
    "plural": false,
    "selections": [
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "ok",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "error",
        "storageKey": null
      }
    ],
    "storageKey": null
  }
];
return {
  "fragment": {
    "argumentDefinitions": (v0/*: any*/),
    "kind": "Fragment",
    "metadata": null,
    "name": "deleteUserMutation",
    "selections": (v1/*: any*/),
    "type": "Mutation",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": (v0/*: any*/),
    "kind": "Operation",
    "name": "deleteUserMutation",
    "selections": (v1/*: any*/)
  },
  "params": {
    "cacheID": "d04ef897956ebf4afe75134542795e01",
    "id": null,
    "metadata": {},
    "name": "deleteUserMutation",
    "operationKind": "mutation",
    "text": "mutation deleteUserMutation(\n  $input: ID!\n) {\n  deleteUser(id: $input) {\n    ok\n    error\n  }\n}\n"
  }
};
})();

(node as any).hash = "75d5cdf07c492b74d05e45e60cc63b0a";

export default node;

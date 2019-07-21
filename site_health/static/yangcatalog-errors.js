'use strict';

import {html, render} from './node_modules/lit-html/lit-html.js';

export class YangCatalogErrors extends HTMLElement {

    constructor() {
        super();
        this._runs = [];
        this.attachShadow({mode: 'open'});
    }

    connectedCallback() {
        this._load().catch(console.log);
    }

    async _load() {
        const resp = await fetch('/errors');
        const data = await resp.json();
        this._errors = data.errors;
        this._invalidate();
    }

    _invalidate() {
        render(this._render(), this.shadowRoot);
    }

    _render() {
        return html`
         <ol>
         ${this._errors.map((err)  => html`
           <li>
            ${err.name}
            <ul>
                <li>Result: ${err.status_code}</li>
                <li>Timestamp: ${err.timestamp}</li>
            </ul>
           </li>
          `)}
         </ol>
        `;
    }
}

customElements.define('yangcatalog-errors', YangCatalogErrors);

'use strict';

import {html, render} from './node_modules/lit-html/lit-html.js';

export class YangCatalogNav extends HTMLElement {

    constructor() {
        super();
        this._runs = [];
        this.attachShadow({mode: 'open'});
    }

    connectedCallback() {
        render(this._render(), this.shadowRoot);
    }

    _render() {
        return html`
        <ul>
            <li>
                <a href="errors.html">Errors</a>
            </li>
            <li>
                <a href="index.html">Runs</a>
            </li>
        </ul>
        `;
    }
}

customElements.define('yangcatalog-nav', YangCatalogNav);


'use strict';

import {html, render} from './node_modules/lit-html/lit-html.js';

export class YangCatalogRun extends HTMLElement {

    constructor() {
        super();
        this._runs = [];
        this.attachShadow({mode: 'open'});
    }

    static get observedAttributes() {
        return ['run-id'];
    }      

    attributeChangedCallback(name, oldValue, newValue) {
        this._load();      
    }

    get run_id() {
        return this.getAttribute('run-id');
    }

    async _load() {
        if (this.run_id == null) {
            return
        }
        const resp = await fetch('/run/' + this.run_id);
        this._run = await resp.json();
        this._invalidate();
    }

    _invalidate() {        
        render(this._render(), this.shadowRoot);
    }

    _render() {
        return html`
          <ul>
            ${this._run.endpoint_tests.map(test => html`
                <li>
                   ${test.name}
                    <ul>
                        <li>Result: ${test.status_code}</li>
                        <li>Duration: ${test.duration}</li>
                    </ul>
                </li>
            `)}
          </ul>
        `;
    }
}

customElements.define('yangcatalog-run', YangCatalogRun);

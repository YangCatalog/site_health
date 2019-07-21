'use strict';

import {html, render} from './node_modules/lit-html/lit-html.js';
import './yangcatalog-run.js';

export class YangCatalogRuns extends HTMLElement {

    constructor() {
        super();
        this._runs = [];
        this.attachShadow({mode: 'open'});
    }

    connectedCallback() {
        this._invalidate();
        this._load().catch(console.log);
    }

    async _load() {
        const resp = await fetch('/run');
        const data = await resp.json();
        this._runs = data.runs;
        this._invalidate();
    }

    _invalidate() {
        render(this._render(), this.shadowRoot);
    }

    _toggleRun(run) {
        console.log("here");
        if (run.show) {
            run.show = false;
        } else {
            run.show = true;
        }
        this._invalidate();
    }

    _render() {
        return html`
         <ol>
         ${this._runs.map((run)  => html`
           <li>
             <a href=# @click="${() => this._toggleRun(run)}">${run.run_id}</a> - ${run.timestamp}
             <div>
               ${run.show
                  ? html`<yangcatalog-run run-id=${run.run_id}></yangcatalog-run>`
                  : ''
                }
             </div>
           </li>
          `)}
         </ol>
        `;
    }
}

customElements.define('yangcatalog-runs', YangCatalogRuns);

const t=globalThis,e=t.ShadowRoot&&(void 0===t.ShadyCSS||t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),s=new WeakMap;let n=class{constructor(t,e,s){if(this._$cssResult$=!0,s!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const i=this.t;if(e&&void 0===t){const e=void 0!==i&&1===i.length;e&&(t=s.get(i)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),e&&s.set(i,t))}return t}toString(){return this.cssText}};const r=(t,...e)=>{const s=1===t.length?t[0]:e.reduce((e,i,s)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[s+1],t[0]);return new n(s,t,i)},a=e?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new n("string"==typeof t?t:t+"",void 0,i))(e)})(t):t,{is:o,defineProperty:c,getOwnPropertyDescriptor:l,getOwnPropertyNames:h,getOwnPropertySymbols:d,getPrototypeOf:p}=Object,u=globalThis,g=u.trustedTypes,f=g?g.emptyScript:"",_=u.reactiveElementPolyfillSupport,m=(t,e)=>t,v={toAttribute(t,e){switch(e){case Boolean:t=t?f:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},y=(t,e)=>!o(t,e),$={attribute:!0,type:String,converter:v,reflect:!1,useDefault:!1,hasChanged:y};Symbol.metadata??=Symbol("metadata"),u.litPropertyMetadata??=new WeakMap;let b=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=$){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(t,i,e);void 0!==s&&c(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){const{get:s,set:n}=l(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:s,set(e){const r=s?.call(this);n?.call(this,e),this.requestUpdate(t,r,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??$}static _$Ei(){if(this.hasOwnProperty(m("elementProperties")))return;const t=p(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(m("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(m("properties"))){const t=this.properties,e=[...h(t),...d(t)];for(const i of e)this.createProperty(i,t[i])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,i]of e)this.elementProperties.set(t,i)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const i=this._$Eu(t,e);void 0!==i&&this._$Eh.set(i,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(a(t))}else void 0!==t&&e.push(a(t));return e}static _$Eu(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const i of e.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const i=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((i,s)=>{if(e)i.adoptedStyleSheets=s.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const e of s){const s=document.createElement("style"),n=t.litNonce;void 0!==n&&s.setAttribute("nonce",n),s.textContent=e.cssText,i.appendChild(s)}})(i,this.constructor.elementStyles),i}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$ET(t,e){const i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(void 0!==s&&!0===i.reflect){const n=(void 0!==i.converter?.toAttribute?i.converter:v).toAttribute(e,i.type);this._$Em=t,null==n?this.removeAttribute(s):this.setAttribute(s,n),this._$Em=null}}_$AK(t,e){const i=this.constructor,s=i._$Eh.get(t);if(void 0!==s&&this._$Em!==s){const t=i.getPropertyOptions(s),n="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:v;this._$Em=s;const r=n.fromAttribute(e,t.type);this[s]=r??this._$Ej?.get(s)??r,this._$Em=null}}requestUpdate(t,e,i){if(void 0!==t){const s=this.constructor,n=this[t];if(i??=s.getPropertyOptions(t),!((i.hasChanged??y)(n,e)||i.useDefault&&i.reflect&&n===this._$Ej?.get(t)&&!this.hasAttribute(s._$Eu(t,i))))return;this.C(t,e,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:i,reflect:s,wrapped:n},r){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,r??e??this[t]),!0!==n||void 0!==r)||(this._$AL.has(t)||(this.hasUpdated||i||(e=void 0),this._$AL.set(t,e)),!0===s&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,i]of t){const{wrapped:t}=i,s=this[e];!0!==t||this._$AL.has(e)||void 0===s||this.C(e,void 0,i,s)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};b.elementStyles=[],b.shadowRootOptions={mode:"open"},b[m("elementProperties")]=new Map,b[m("finalized")]=new Map,_?.({ReactiveElement:b}),(u.reactiveElementVersions??=[]).push("2.1.1");const w=globalThis,x=w.trustedTypes,A=x?x.createPolicy("lit-html",{createHTML:t=>t}):void 0,S="$lit$",E=`lit$${Math.random().toFixed(9).slice(2)}$`,C="?"+E,k=`<${C}>`,U=document,P=()=>U.createComment(""),M=t=>null===t||"object"!=typeof t&&"function"!=typeof t,O=Array.isArray,T="[ \t\n\f\r]",R=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,H=/-->/g,N=/>/g,z=RegExp(`>|${T}(?:([^\\s"'>=/]+)(${T}*=${T}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),I=/'/g,j=/"/g,D=/^(?:script|style|textarea|title)$/i,L=(t=>(e,...i)=>({_$litType$:t,strings:e,values:i}))(1),V=Symbol.for("lit-noChange"),B=Symbol.for("lit-nothing"),W=new WeakMap,q=U.createTreeWalker(U,129);function F(t,e){if(!O(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==A?A.createHTML(e):e}const Y=(t,e)=>{const i=t.length-1,s=[];let n,r=2===e?"<svg>":3===e?"<math>":"",a=R;for(let e=0;e<i;e++){const i=t[e];let o,c,l=-1,h=0;for(;h<i.length&&(a.lastIndex=h,c=a.exec(i),null!==c);)h=a.lastIndex,a===R?"!--"===c[1]?a=H:void 0!==c[1]?a=N:void 0!==c[2]?(D.test(c[2])&&(n=RegExp("</"+c[2],"g")),a=z):void 0!==c[3]&&(a=z):a===z?">"===c[0]?(a=n??R,l=-1):void 0===c[1]?l=-2:(l=a.lastIndex-c[2].length,o=c[1],a=void 0===c[3]?z:'"'===c[3]?j:I):a===j||a===I?a=z:a===H||a===N?a=R:(a=z,n=void 0);const d=a===z&&t[e+1].startsWith("/>")?" ":"";r+=a===R?i+k:l>=0?(s.push(o),i.slice(0,l)+S+i.slice(l)+E+d):i+E+(-2===l?e:d)}return[F(t,r+(t[i]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),s]};class G{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let n=0,r=0;const a=t.length-1,o=this.parts,[c,l]=Y(t,e);if(this.el=G.createElement(c,i),q.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(s=q.nextNode())&&o.length<a;){if(1===s.nodeType){if(s.hasAttributes())for(const t of s.getAttributeNames())if(t.endsWith(S)){const e=l[r++],i=s.getAttribute(t).split(E),a=/([.?@])?(.*)/.exec(e);o.push({type:1,index:n,name:a[2],strings:i,ctor:"."===a[1]?X:"?"===a[1]?tt:"@"===a[1]?et:Q}),s.removeAttribute(t)}else t.startsWith(E)&&(o.push({type:6,index:n}),s.removeAttribute(t));if(D.test(s.tagName)){const t=s.textContent.split(E),e=t.length-1;if(e>0){s.textContent=x?x.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],P()),q.nextNode(),o.push({type:2,index:++n});s.append(t[e],P())}}}else if(8===s.nodeType)if(s.data===C)o.push({type:2,index:n});else{let t=-1;for(;-1!==(t=s.data.indexOf(E,t+1));)o.push({type:7,index:n}),t+=E.length-1}n++}}static createElement(t,e){const i=U.createElement("template");return i.innerHTML=t,i}}function J(t,e,i=t,s){if(e===V)return e;let n=void 0!==s?i._$Co?.[s]:i._$Cl;const r=M(e)?void 0:e._$litDirective$;return n?.constructor!==r&&(n?._$AO?.(!1),void 0===r?n=void 0:(n=new r(t),n._$AT(t,i,s)),void 0!==s?(i._$Co??=[])[s]=n:i._$Cl=n),void 0!==n&&(e=J(t,n._$AS(t,e.values),n,s)),e}class K{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:i}=this._$AD,s=(t?.creationScope??U).importNode(e,!0);q.currentNode=s;let n=q.nextNode(),r=0,a=0,o=i[0];for(;void 0!==o;){if(r===o.index){let e;2===o.type?e=new Z(n,n.nextSibling,this,t):1===o.type?e=new o.ctor(n,o.name,o.strings,this,t):6===o.type&&(e=new it(n,this,t)),this._$AV.push(e),o=i[++a]}r!==o?.index&&(n=q.nextNode(),r++)}return q.currentNode=U,s}p(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class Z{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,i,s){this.type=2,this._$AH=B,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=J(this,t,e),M(t)?t===B||null==t||""===t?(this._$AH!==B&&this._$AR(),this._$AH=B):t!==this._$AH&&t!==V&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>O(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==B&&M(this._$AH)?this._$AA.nextSibling.data=t:this.T(U.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:i}=t,s="number"==typeof i?this._$AC(t):(void 0===i.el&&(i.el=G.createElement(F(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(e);else{const t=new K(s,this),i=t.u(this.options);t.p(e),this.T(i),this._$AH=t}}_$AC(t){let e=W.get(t.strings);return void 0===e&&W.set(t.strings,e=new G(t)),e}k(t){O(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,s=0;for(const n of t)s===e.length?e.push(i=new Z(this.O(P()),this.O(P()),this,this.options)):i=e[s],i._$AI(n),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=t.nextSibling;t.remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class Q{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,i,s,n){this.type=1,this._$AH=B,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=n,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=B}_$AI(t,e=this,i,s){const n=this.strings;let r=!1;if(void 0===n)t=J(this,t,e,0),r=!M(t)||t!==this._$AH&&t!==V,r&&(this._$AH=t);else{const s=t;let a,o;for(t=n[0],a=0;a<n.length-1;a++)o=J(this,s[i+a],e,a),o===V&&(o=this._$AH[a]),r||=!M(o)||o!==this._$AH[a],o===B?t=B:t!==B&&(t+=(o??"")+n[a+1]),this._$AH[a]=o}r&&!s&&this.j(t)}j(t){t===B?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class X extends Q{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===B?void 0:t}}class tt extends Q{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==B)}}class et extends Q{constructor(t,e,i,s,n){super(t,e,i,s,n),this.type=5}_$AI(t,e=this){if((t=J(this,t,e,0)??B)===V)return;const i=this._$AH,s=t===B&&i!==B||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,n=t!==B&&(i===B||s);s&&this.element.removeEventListener(this.name,this,i),n&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class it{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){J(this,t)}}const st=w.litHtmlPolyfillSupport;st?.(G,Z),(w.litHtmlVersions??=[]).push("3.3.1");const nt=globalThis;class rt extends b{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{const s=i?.renderBefore??e;let n=s._$litPart$;if(void 0===n){const t=i?.renderBefore??null;s._$litPart$=n=new Z(e.insertBefore(P(),t),t,void 0,i??{})}return n._$AI(t),n})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return V}}rt._$litElement$=!0,rt.finalized=!0,nt.litElementHydrateSupport?.({LitElement:rt});const at=nt.litElementPolyfillSupport;at?.({LitElement:rt}),(nt.litElementVersions??=[]).push("4.2.1");const ot=r`
  :host {
    --sac-primary-color: var(--primary-color, #03a9f4);
    --sac-text-primary: var(--primary-text-color, #212121);
    --sac-text-secondary: var(--secondary-text-color, #727272);
    --sac-card-background: var(--card-background-color, #fff);
    --sac-divider-color: var(--divider-color, rgba(0, 0, 0, 0.12));
    --sac-border-radius: var(--ha-card-border-radius, 12px);
    --sac-spacing: 16px;
    --sac-spacing-sm: 8px;
    --sac-spacing-lg: 24px;
    
    /* State colors */
    --sac-state-idle: var(--state-inactive-color, #9e9e9e);
    --sac-state-running: var(--state-active-color, #4caf50);
    --sac-state-finished: var(--state-finished-color, #2196f3);
    --sac-state-alert: var(--warning-color, #ff9800);
    --sac-state-error: var(--error-color, #f44336);
    
    /* Shadows */
    --sac-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12);
    --sac-shadow-md: 0 2px 8px rgba(0, 0, 0, 0.15);
    --sac-shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.2);
    
    /* Transitions */
    --sac-transition-fast: 150ms ease-out;
    --sac-transition-normal: 300ms ease-out;
    --sac-transition-slow: 500ms ease-out;
  }
  
  /* Card container */
  .card {
    background: var(--sac-card-background);
    border-radius: var(--sac-border-radius);
    padding: var(--sac-spacing);
    box-shadow: var(--sac-shadow-sm);
    position: relative;
    overflow: hidden;
  }
  
  /* Card header */
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--sac-spacing);
  }
  
  .card-title {
    font-size: 20px;
    font-weight: 500;
    color: var(--sac-text-primary);
    margin: 0;
    display: flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
  }
  
  /* Icon styles */
  ha-icon {
    color: var(--sac-text-secondary);
  }
  
  .icon-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: var(--sac-spacing-sm);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color var(--sac-transition-fast);
  }
  
  .icon-button:hover {
    background-color: rgba(0, 0, 0, 0.05);
  }
  
  .icon-button:active {
    background-color: rgba(0, 0, 0, 0.1);
  }
  
  /* Status indicators */
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
    padding: 6px 12px;
    border-radius: 16px;
    font-size: 14px;
    font-weight: 500;
    text-transform: capitalize;
  }
  
  .status-badge.idle {
    background-color: rgba(158, 158, 158, 0.1);
    color: var(--sac-state-idle);
  }
  
  .status-badge.running {
    background-color: rgba(76, 175, 80, 0.1);
    color: var(--sac-state-running);
  }
  
  .status-badge.finished {
    background-color: rgba(33, 150, 243, 0.1);
    color: var(--sac-state-finished);
  }
  
  /* Value displays */
  .value-container {
    display: flex;
    flex-direction: column;
    gap: var(--sac-spacing-sm);
  }
  
  .value-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--sac-spacing-sm) 0;
  }
  
  .value-label {
    font-size: 14px;
    color: var(--sac-text-secondary);
    display: flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
  }
  
  .value-text {
    font-size: 16px;
    font-weight: 500;
    color: var(--sac-text-primary);
  }
  
  .value-large {
    font-size: 24px;
    font-weight: 600;
  }
  
  /* Divider */
  .divider {
    height: 1px;
    background-color: var(--sac-divider-color);
    margin: var(--sac-spacing) 0;
  }
  
  /* Buttons */
  .button {
    background: var(--sac-primary-color);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--sac-transition-fast);
    display: flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
  }
  
  .button:hover {
    opacity: 0.9;
    box-shadow: var(--sac-shadow-md);
  }
  
  .button:active {
    transform: scale(0.98);
  }
  
  .button-secondary {
    background: transparent;
    color: var(--sac-primary-color);
    border: 1px solid var(--sac-primary-color);
  }
  
  .button-danger {
    background: var(--sac-state-error);
  }
  
  .button-group {
    display: flex;
    gap: var(--sac-spacing-sm);
    flex-wrap: wrap;
  }
  
  /* Alert/Warning states */
  .alert-container {
    padding: var(--sac-spacing-sm);
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
    margin-bottom: var(--sac-spacing);
  }
  
  .alert-warning {
    background-color: rgba(255, 152, 0, 0.1);
    border-left: 4px solid var(--sac-state-alert);
  }
  
  .alert-error {
    background-color: rgba(244, 67, 54, 0.1);
    border-left: 4px solid var(--sac-state-error);
  }
  
  .alert-info {
    background-color: rgba(33, 150, 243, 0.1);
    border-left: 4px solid var(--sac-state-finished);
  }
  
  /* Loading state */
  .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--sac-spacing-lg);
    color: var(--sac-text-secondary);
  }
  
  /* Animations */
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
  
  @keyframes rotate {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .pulse {
    animation: pulse 2s ease-in-out infinite;
  }
  
  .rotate {
    animation: rotate 2s linear infinite;
  }
  
  .fade-in {
    animation: fadeIn var(--sac-transition-normal) ease-out;
  }
  
  /* Grid layouts */
  .grid {
    display: grid;
    gap: var(--sac-spacing);
  }
  
  .grid-2 {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .grid-3 {
    grid-template-columns: repeat(3, 1fr);
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .card {
      padding: var(--sac-spacing-sm);
    }
    
    .card-title {
      font-size: 18px;
    }
    
    .value-large {
      font-size: 20px;
    }
    
    .grid-2,
    .grid-3 {
      grid-template-columns: 1fr;
    }
  }
  
  @media (max-width: 480px) {
    :host {
      --sac-spacing: 12px;
      --sac-spacing-sm: 6px;
    }
    
    .button-group {
      flex-direction: column;
    }
    
    .button {
      width: 100%;
      justify-content: center;
    }
  }
`,ct="idle",lt="running",ht="finished",dt="unknown",pt={idle:"#9e9e9e",running:"#4caf50",finished:"#2196f3",unknown:"#ff9800"},ut={idle:"mdi:power-standby",running:"mdi:play-circle",finished:"mdi:check-circle",unknown:"mdi:help-circle"},gt={washing_machine:"cycle",dishwasher:"cycle",dryer:"cycle",oven:"cycle",water_heater:"cycle",coffee_maker:"cycle",monitor:"session",nas:"session",printer_3d:"session",vmc:"session",generic:"cycle"},ft={washing_machine:"mdi:washing-machine",dishwasher:"mdi:dishwasher",dryer:"mdi:tumble-dryer",oven:"mdi:stove",water_heater:"mdi:water-boiler",coffee_maker:"mdi:coffee-maker",monitor:"mdi:monitor",nas:"mdi:nas",printer_3d:"mdi:printer-3d",vmc:"mdi:fan",generic:"mdi:power-plug"},_t={show_power_graph:!0,show_action_buttons:!0,show_current_power:!1,graph_hours:.5,theme:"auto"},mt=1e3;function vt(t,e){if(!t||!e)return null;const i=t.states[e];return i?i.state:null}function yt(t,e){const i=vt(t,e);if(null===i||"unknown"===i||"unavailable"===i)return null;const s=parseFloat(i);return isNaN(s)?null:s}function $t(t,e,i,s={}){t&&t.callService(e,i,s)}customElements.define("smart-appliance-cycle-card-editor",class extends rt{static get properties(){return{hass:{type:Object},config:{type:Object}}}setConfig(t){this.config=t}_valueChanged(t){if(!this.config||!this.hass)return;const e=t.target,i="checkbox"===e.type?e.checked:e.value;if(this.config[e.configValue]===i)return;!function(t,e,i={}){const s=new Event(e,{bubbles:!0,composed:!0,cancelable:!1});s.detail=i,t.dispatchEvent(s)}(this,"config-changed",{config:{...this.config,[e.configValue]:i}})}render(){return this.hass&&this.config?L`
      <div class="card-config">
        <div class="config-section">
          <div class="config-label">Entity (required)</div>
          <ha-entity-picker
            .hass=${this.hass}
            .value=${this.config.entity}
            .configValue=${"entity"}
            @value-changed=${this._valueChanged}
            .includeDomains=${["sensor"]}
            allow-custom-entity
          ></ha-entity-picker>
          <div class="config-hint">Select the state sensor (e.g., sensor.washing_machine_state)</div>
        </div>

        <div class="config-section">
          <div class="config-label">Name (optional)</div>
          <ha-textfield
            .value=${this.config.name||""}
            .configValue=${"name"}
            @input=${this._valueChanged}
            placeholder="Auto-detected from entity"
          ></ha-textfield>
        </div>

        <div class="config-section">
          <div class="config-label">Icon (optional)</div>
          <ha-icon-picker
            .hass=${this.hass}
            .value=${this.config.icon||""}
            .configValue=${"icon"}
            @value-changed=${this._valueChanged}
            placeholder="Auto-detected from appliance type"
          ></ha-icon-picker>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <ha-formfield label="Show power graph">
            <ha-switch
              .checked=${!1!==this.config.show_power_graph}
              .configValue=${"show_power_graph"}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Display mini graph of power consumption</div>
        </div>

        <div class="config-section">
          <ha-formfield label="Show action buttons">
            <ha-switch
              .checked=${!1!==this.config.show_action_buttons}
              .configValue=${"show_action_buttons"}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Show start, stop, and reset buttons</div>
        </div>

        <div class="config-section">
          <ha-formfield label="Show current power">
            <ha-switch
              .checked=${!0===this.config.show_current_power}
              .configValue=${"show_current_power"}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Display current power consumption value</div>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <div class="config-label">Graph duration (hours)</div>
          <ha-slider
            .value=${this.config.graph_hours||.5}
            .configValue=${"graph_hours"}
            @change=${this._valueChanged}
            min="0.25"
            max="2"
            step="0.25"
            labeled
          ></ha-slider>
          <div class="config-hint">Time range for power graph: ${this.config.graph_hours||.5}h</div>
        </div>

        <div class="config-section">
          <div class="config-label">Theme</div>
          <ha-select
            .value=${this.config.theme||"auto"}
            .configValue=${"theme"}
            @selected=${this._valueChanged}
          >
            <mwc-list-item value="auto">Auto (follow HA theme)</mwc-list-item>
            <mwc-list-item value="light">Light</mwc-list-item>
            <mwc-list-item value="dark">Dark</mwc-list-item>
          </ha-select>
        </div>
      </div>
    `:L``}static get styles(){return r`
      .card-config {
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding: 16px;
      }

      .config-section {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .config-label {
        font-weight: 500;
        color: var(--primary-text-color);
      }

      .config-hint {
        font-size: 12px;
        color: var(--secondary-text-color);
        font-style: italic;
      }

      .config-divider {
        height: 1px;
        background-color: var(--divider-color);
        margin: 8px 0;
      }

      ha-formfield {
        display: flex;
        align-items: center;
      }

      ha-textfield,
      ha-entity-picker,
      ha-icon-picker,
      ha-select {
        width: 100%;
      }

      ha-slider {
        width: 100%;
      }
    `}});customElements.define("smart-appliance-cycle-card",class extends rt{static get properties(){return{hass:{type:Object},config:{type:Object},_entities:{type:Object},_applianceType:{type:String},_terminology:{type:String},_updateInterval:{type:Number}}}static getConfigElement(){return document.createElement("smart-appliance-cycle-card-editor")}static getStubConfig(){return{entity:"sensor.washing_machine_state",show_power_graph:!0,show_action_buttons:!0,show_current_power:!1,graph_hours:.5,theme:"auto"}}constructor(){super(),this._entities=null,this._applianceType="generic",this._terminology="cycle",this._updateInterval=null}setConfig(t){if(!t.entity)throw new Error("You need to define an entity");this.config={..._t,...t}}connectedCallback(){super.connectedCallback(),this._startAutoUpdate()}disconnectedCallback(){super.disconnectedCallback(),this._stopAutoUpdate()}updated(t){var e;super.updated(t),(t.has("hass")||t.has("config"))&&this.hass&&this.config?.entity&&(this._entities=function(t,e){if(!e||!t)return null;const i=e.match(/^sensor\.(.+)_state$/);if(!i)return null;const s=i[1];return{state:e,cycle_duration:`sensor.${s}_cycle_duration`,cycle_energy:`sensor.${s}_cycle_energy`,cycle_cost:`sensor.${s}_cycle_cost`,last_cycle_duration:`sensor.${s}_last_cycle_duration`,last_cycle_energy:`sensor.${s}_last_cycle_energy`,last_cycle_cost:`sensor.${s}_last_cycle_cost`,daily_cycles:`sensor.${s}_daily_cycles`,daily_cost:`sensor.${s}_daily_cost`,monthly_cost:`sensor.${s}_monthly_cost`,running:`binary_sensor.${s}_running`,duration_alert:`binary_sensor.${s}_duration_alert`,unplugged:`binary_sensor.${s}_unplugged`,monitoring:`switch.${s}_monitoring`,notifications:`switch.${s}_notifications`,notify_started:`switch.${s}_notify_cycle_started`,notify_finished:`switch.${s}_notify_cycle_finished`,notify_alert:`switch.${s}_notify_alert_duration`,notify_unplugged:`switch.${s}_notify_unplugged`,reset_stats:`button.${s}_reset_statistics`}}(this.hass,this.config.entity),this._applianceType=function(t,e){if(!t||!e)return"generic";const i=t.states[e];if(!i)return"generic";const s=i.attributes?.appliance_type;if(s)return s;const n=e.toLowerCase();return n.includes("washing")?"washing_machine":n.includes("dishwasher")?"dishwasher":n.includes("dryer")?"dryer":n.includes("oven")?"oven":n.includes("water")&&n.includes("heater")?"water_heater":n.includes("coffee")?"coffee_maker":n.includes("monitor")||n.includes("screen")?"monitor":n.includes("nas")?"nas":n.includes("printer")&&n.includes("3d")?"printer_3d":n.includes("vmc")||n.includes("ventilation")?"vmc":"generic"}(this.hass,this.config.entity),this._terminology=(e=this._applianceType,gt[e]||"cycle"))}_startAutoUpdate(){this._stopAutoUpdate(),this._updateInterval=setInterval(()=>{this.requestUpdate()},mt)}_stopAutoUpdate(){this._updateInterval&&(clearInterval(this._updateInterval),this._updateInterval=null)}_getState(){if(!this._entities)return dt;return vt(this.hass,this._entities.state)||dt}_isRunning(){return this._getState()===lt}_isFinished(){return this._getState()===ht}_isIdle(){return this._getState()===ct}_isUnplugged(){return!!this._entities&&"on"===vt(this.hass,this._entities.unplugged)}_hasAlert(){return!!this._entities&&"on"===vt(this.hass,this._entities.duration_alert)}_isMonitoring(){return!this._entities||"on"===vt(this.hass,this._entities.monitoring)}_getCurrentDuration(){return this._entities&&yt(this.hass,this._entities.cycle_duration)||0}_getCurrentEnergy(){return this._entities&&yt(this.hass,this._entities.cycle_energy)||0}_getCurrentCost(){return this._entities&&yt(this.hass,this._entities.cycle_cost)||0}_handleStopMonitoring(){this._entities&&$t(this.hass,"switch","turn_off",{entity_id:this._entities.monitoring})}_handleResetStats(){this._entities&&$t(this.hass,"button","press",{entity_id:this._entities.reset_stats})}_handleStartCycle(){if(!this.config.entity)return;const t=this.config.entity.replace("sensor.","").replace("_state","");$t(this.hass,"smart_appliance_monitor","start_cycle",{entity_id:`sensor.${t}_state`})}_renderStatusIndicator(){const t=this._getState(),e=ut[t]||ut.unknown,i=pt[t]||pt.unknown,s=this._isRunning();return L`
      <div class="status-indicator ${s?"pulse":""}">
        <div 
          class="status-circle" 
          style="background-color: ${i};"
        >
          <ha-icon 
            icon="${e}"
            class="${s?"rotate":""}"
          ></ha-icon>
        </div>
        <div class="status-text">
          <div class="status-label">${t}</div>
          <div class="status-sublabel">${this._terminology}</div>
        </div>
      </div>
    `}_renderCurrentValues(){const t=this._getCurrentDuration(),e=this._getCurrentEnergy(),i=this._getCurrentCost();return L`
      <div class="current-values">
        <div class="value-row">
          <span class="value-label">
            <ha-icon icon="mdi:timer-outline"></ha-icon>
            Duration
          </span>
          <span class="value-text">${function(t,e=!1){if(!t||t<0)return"0s";const i=Math.floor(t/3600),s=Math.floor(t%3600/60),n=Math.floor(t%60),r=[];return i>0&&r.push(`${i}h`),s>0&&r.push(`${s}m`),!e&&n>0&&0===i&&r.push(`${n}s`),r.length>0?r.join(" "):"0s"}(t)}</span>
        </div>
        
        <div class="value-row">
          <span class="value-label">
            <ha-icon icon="mdi:lightning-bolt"></ha-icon>
            Energy
          </span>
          <span class="value-text">${function(t,e=2){if(!t||t<0)return"0 kWh";if(t<1)return`${Math.round(1e3*t)} Wh`;return`${t.toFixed(e)} kWh`}(e)}</span>
        </div>
        
        <div class="value-row">
          <span class="value-label">
            <ha-icon icon="mdi:currency-eur"></ha-icon>
            Cost
          </span>
          <span class="value-text">${function(t,e="€",i=2){return!t||t<0?`0.00 ${e}`:`${t.toFixed(i)} ${e}`}(i)}</span>
        </div>
      </div>
    `}_renderActionButtons(){if(!this.config.show_action_buttons)return L``;const t=this._getState(),e=t===ct||t===ht;return L`
      <div class="action-buttons">
        ${t===ct?L`
          <button class="button" @click="${this._handleStartCycle}">
            <ha-icon icon="mdi:play"></ha-icon>
            Start ${this._terminology}
          </button>
        `:""}
        
        ${this._isRunning()?L`
          <button class="button button-danger" @click="${this._handleStopMonitoring}">
            <ha-icon icon="mdi:stop"></ha-icon>
            Stop Monitoring
          </button>
        `:""}
        
        ${e?L`
          <button class="button button-secondary" @click="${this._handleResetStats}">
            <ha-icon icon="mdi:refresh"></ha-icon>
            Reset Stats
          </button>
        `:""}
      </div>
    `}_renderAlerts(){const t=[];return this._isUnplugged()&&t.push(L`
        <div class="alert-container alert-error">
          <ha-icon icon="mdi:power-plug-off"></ha-icon>
          <span>Appliance is unplugged or powered off</span>
        </div>
      `),this._hasAlert()&&t.push(L`
        <div class="alert-container alert-warning">
          <ha-icon icon="mdi:alert"></ha-icon>
          <span>${this._terminology} duration exceeds expected time</span>
        </div>
      `),this._isMonitoring()||this._isUnplugged()||t.push(L`
        <div class="alert-container alert-info">
          <ha-icon icon="mdi:information"></ha-icon>
          <span>Monitoring is currently disabled</span>
        </div>
      `),t}render(){if(!this.hass||!this.config)return L`<div class="loading">Loading...</div>`;if(!this._entities)return L`
        <ha-card>
          <div class="card">
            <div class="alert-container alert-error">
              <ha-icon icon="mdi:alert-circle"></ha-icon>
              <span>Entity not found: ${this.config.entity}</span>
            </div>
          </div>
        </ha-card>
      `;const t=this.config.name||this.hass.states[this.config.entity]?.attributes?.friendly_name||"Appliance",e=this.config.icon||(i=this._applianceType,ft[i]||ft.generic);var i;return L`
      <ha-card>
        <div class="card fade-in">
          <div class="card-header">
            <h2 class="card-title">
              <ha-icon icon="${e}"></ha-icon>
              ${t}
            </h2>
          </div>

          ${this._renderAlerts()}
          
          ${this._renderStatusIndicator()}
          
          <div class="divider"></div>
          
          ${this._renderCurrentValues()}
          
          ${this._renderActionButtons()}
        </div>
      </ha-card>
    `}static get styles(){return[ot,r`
        :host {
          display: block;
        }

        ha-card {
          height: 100%;
        }

        .status-indicator {
          display: flex;
          align-items: center;
          gap: var(--sac-spacing);
          margin: var(--sac-spacing) 0;
        }

        .status-circle {
          width: 80px;
          height: 80px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: var(--sac-shadow-md);
        }

        .status-circle ha-icon {
          --mdc-icon-size: 40px;
          color: white;
        }

        .status-text {
          flex: 1;
        }

        .status-label {
          font-size: 24px;
          font-weight: 600;
          color: var(--sac-text-primary);
          text-transform: capitalize;
        }

        .status-sublabel {
          font-size: 14px;
          color: var(--sac-text-secondary);
          text-transform: capitalize;
        }

        .current-values {
          margin: var(--sac-spacing) 0;
        }

        .action-buttons {
          display: flex;
          flex-direction: column;
          gap: var(--sac-spacing-sm);
          margin-top: var(--sac-spacing);
        }

        @media (max-width: 480px) {
          .status-circle {
            width: 60px;
            height: 60px;
          }

          .status-circle ha-icon {
            --mdc-icon-size: 30px;
          }

          .status-label {
            font-size: 20px;
          }
        }
      `]}getCardSize(){return 4}}),window.customCards=window.customCards||[],window.customCards.push({type:"smart-appliance-cycle-card",name:"Smart Appliance Cycle Card",description:"Display current cycle/session with visual progress",preview:!0,documentationURL:"https://github.com/legaetan/ha-smart_appliance_monitor/wiki"});

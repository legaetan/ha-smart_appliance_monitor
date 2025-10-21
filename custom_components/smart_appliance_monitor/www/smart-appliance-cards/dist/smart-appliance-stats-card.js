const t=globalThis,e=t.ShadowRoot&&(void 0===t.ShadyCSS||t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),s=new WeakMap;let a=class{constructor(t,e,s){if(this._$cssResult$=!0,s!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const i=this.t;if(e&&void 0===t){const e=void 0!==i&&1===i.length;e&&(t=s.get(i)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),e&&s.set(i,t))}return t}toString(){return this.cssText}};const n=(t,...e)=>{const s=1===t.length?t[0]:e.reduce((e,i,s)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[s+1],t[0]);return new a(s,t,i)},r=e?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new a("string"==typeof t?t:t+"",void 0,i))(e)})(t):t,{is:o,defineProperty:c,getOwnPropertyDescriptor:l,getOwnPropertyNames:d,getOwnPropertySymbols:h,getPrototypeOf:p}=Object,u=globalThis,g=u.trustedTypes,v=g?g.emptyScript:"",f=u.reactiveElementPolyfillSupport,_=(t,e)=>t,y={toAttribute(t,e){switch(e){case Boolean:t=t?v:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},m=(t,e)=>!o(t,e),$={attribute:!0,type:String,converter:y,reflect:!1,useDefault:!1,hasChanged:m};Symbol.metadata??=Symbol("metadata"),u.litPropertyMetadata??=new WeakMap;let b=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=$){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(t,i,e);void 0!==s&&c(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){const{get:s,set:a}=l(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:s,set(e){const n=s?.call(this);a?.call(this,e),this.requestUpdate(t,n,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??$}static _$Ei(){if(this.hasOwnProperty(_("elementProperties")))return;const t=p(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(_("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(_("properties"))){const t=this.properties,e=[...d(t),...h(t)];for(const i of e)this.createProperty(i,t[i])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,i]of e)this.elementProperties.set(t,i)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const i=this._$Eu(t,e);void 0!==i&&this._$Eh.set(i,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(r(t))}else void 0!==t&&e.push(r(t));return e}static _$Eu(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const i of e.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const i=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((i,s)=>{if(e)i.adoptedStyleSheets=s.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const e of s){const s=document.createElement("style"),a=t.litNonce;void 0!==a&&s.setAttribute("nonce",a),s.textContent=e.cssText,i.appendChild(s)}})(i,this.constructor.elementStyles),i}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$ET(t,e){const i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(void 0!==s&&!0===i.reflect){const a=(void 0!==i.converter?.toAttribute?i.converter:y).toAttribute(e,i.type);this._$Em=t,null==a?this.removeAttribute(s):this.setAttribute(s,a),this._$Em=null}}_$AK(t,e){const i=this.constructor,s=i._$Eh.get(t);if(void 0!==s&&this._$Em!==s){const t=i.getPropertyOptions(s),a="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:y;this._$Em=s;const n=a.fromAttribute(e,t.type);this[s]=n??this._$Ej?.get(s)??n,this._$Em=null}}requestUpdate(t,e,i){if(void 0!==t){const s=this.constructor,a=this[t];if(i??=s.getPropertyOptions(t),!((i.hasChanged??m)(a,e)||i.useDefault&&i.reflect&&a===this._$Ej?.get(t)&&!this.hasAttribute(s._$Eu(t,i))))return;this.C(t,e,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:i,reflect:s,wrapped:a},n){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,n??e??this[t]),!0!==a||void 0!==n)||(this._$AL.has(t)||(this.hasUpdated||i||(e=void 0),this._$AL.set(t,e)),!0===s&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,i]of t){const{wrapped:t}=i,s=this[e];!0!==t||this._$AL.has(e)||void 0===s||this.C(e,void 0,i,s)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};b.elementStyles=[],b.shadowRootOptions={mode:"open"},b[_("elementProperties")]=new Map,b[_("finalized")]=new Map,f?.({ReactiveElement:b}),(u.reactiveElementVersions??=[]).push("2.1.1");const w=globalThis,x=w.trustedTypes,A=x?x.createPolicy("lit-html",{createHTML:t=>t}):void 0,C="$lit$",E=`lit$${Math.random().toFixed(9).slice(2)}$`,S="?"+E,k=`<${S}>`,T=document,U=()=>T.createComment(""),P=t=>null===t||"object"!=typeof t&&"function"!=typeof t,M=Array.isArray,O="[ \t\n\f\r]",z=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,H=/-->/g,N=/>/g,D=RegExp(`>|${O}(?:([^\\s"'>=/]+)(${O}*=${O}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),L=/'/g,R=/"/g,j=/^(?:script|style|textarea|title)$/i,I=(t=>(e,...i)=>({_$litType$:t,strings:e,values:i}))(1),V=Symbol.for("lit-noChange"),W=Symbol.for("lit-nothing"),B=new WeakMap,q=T.createTreeWalker(T,129);function F(t,e){if(!M(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==A?A.createHTML(e):e}const Y=(t,e)=>{const i=t.length-1,s=[];let a,n=2===e?"<svg>":3===e?"<math>":"",r=z;for(let e=0;e<i;e++){const i=t[e];let o,c,l=-1,d=0;for(;d<i.length&&(r.lastIndex=d,c=r.exec(i),null!==c);)d=r.lastIndex,r===z?"!--"===c[1]?r=H:void 0!==c[1]?r=N:void 0!==c[2]?(j.test(c[2])&&(a=RegExp("</"+c[2],"g")),r=D):void 0!==c[3]&&(r=D):r===D?">"===c[0]?(r=a??z,l=-1):void 0===c[1]?l=-2:(l=r.lastIndex-c[2].length,o=c[1],r=void 0===c[3]?D:'"'===c[3]?R:L):r===R||r===L?r=D:r===H||r===N?r=z:(r=D,a=void 0);const h=r===D&&t[e+1].startsWith("/>")?" ":"";n+=r===z?i+k:l>=0?(s.push(o),i.slice(0,l)+C+i.slice(l)+E+h):i+E+(-2===l?e:h)}return[F(t,n+(t[i]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),s]};class J{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let a=0,n=0;const r=t.length-1,o=this.parts,[c,l]=Y(t,e);if(this.el=J.createElement(c,i),q.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(s=q.nextNode())&&o.length<r;){if(1===s.nodeType){if(s.hasAttributes())for(const t of s.getAttributeNames())if(t.endsWith(C)){const e=l[n++],i=s.getAttribute(t).split(E),r=/([.?@])?(.*)/.exec(e);o.push({type:1,index:a,name:r[2],strings:i,ctor:"."===r[1]?X:"?"===r[1]?tt:"@"===r[1]?et:Q}),s.removeAttribute(t)}else t.startsWith(E)&&(o.push({type:6,index:a}),s.removeAttribute(t));if(j.test(s.tagName)){const t=s.textContent.split(E),e=t.length-1;if(e>0){s.textContent=x?x.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],U()),q.nextNode(),o.push({type:2,index:++a});s.append(t[e],U())}}}else if(8===s.nodeType)if(s.data===S)o.push({type:2,index:a});else{let t=-1;for(;-1!==(t=s.data.indexOf(E,t+1));)o.push({type:7,index:a}),t+=E.length-1}a++}}static createElement(t,e){const i=T.createElement("template");return i.innerHTML=t,i}}function K(t,e,i=t,s){if(e===V)return e;let a=void 0!==s?i._$Co?.[s]:i._$Cl;const n=P(e)?void 0:e._$litDirective$;return a?.constructor!==n&&(a?._$AO?.(!1),void 0===n?a=void 0:(a=new n(t),a._$AT(t,i,s)),void 0!==s?(i._$Co??=[])[s]=a:i._$Cl=a),void 0!==a&&(e=K(t,a._$AS(t,e.values),a,s)),e}class Z{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:i}=this._$AD,s=(t?.creationScope??T).importNode(e,!0);q.currentNode=s;let a=q.nextNode(),n=0,r=0,o=i[0];for(;void 0!==o;){if(n===o.index){let e;2===o.type?e=new G(a,a.nextSibling,this,t):1===o.type?e=new o.ctor(a,o.name,o.strings,this,t):6===o.type&&(e=new it(a,this,t)),this._$AV.push(e),o=i[++r]}n!==o?.index&&(a=q.nextNode(),n++)}return q.currentNode=T,s}p(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class G{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,i,s){this.type=2,this._$AH=W,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=K(this,t,e),P(t)?t===W||null==t||""===t?(this._$AH!==W&&this._$AR(),this._$AH=W):t!==this._$AH&&t!==V&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>M(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==W&&P(this._$AH)?this._$AA.nextSibling.data=t:this.T(T.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:i}=t,s="number"==typeof i?this._$AC(t):(void 0===i.el&&(i.el=J.createElement(F(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(e);else{const t=new Z(s,this),i=t.u(this.options);t.p(e),this.T(i),this._$AH=t}}_$AC(t){let e=B.get(t.strings);return void 0===e&&B.set(t.strings,e=new J(t)),e}k(t){M(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,s=0;for(const a of t)s===e.length?e.push(i=new G(this.O(U()),this.O(U()),this,this.options)):i=e[s],i._$AI(a),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=t.nextSibling;t.remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class Q{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,i,s,a){this.type=1,this._$AH=W,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=a,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=W}_$AI(t,e=this,i,s){const a=this.strings;let n=!1;if(void 0===a)t=K(this,t,e,0),n=!P(t)||t!==this._$AH&&t!==V,n&&(this._$AH=t);else{const s=t;let r,o;for(t=a[0],r=0;r<a.length-1;r++)o=K(this,s[i+r],e,r),o===V&&(o=this._$AH[r]),n||=!P(o)||o!==this._$AH[r],o===W?t=W:t!==W&&(t+=(o??"")+a[r+1]),this._$AH[r]=o}n&&!s&&this.j(t)}j(t){t===W?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class X extends Q{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===W?void 0:t}}class tt extends Q{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==W)}}class et extends Q{constructor(t,e,i,s,a){super(t,e,i,s,a),this.type=5}_$AI(t,e=this){if((t=K(this,t,e,0)??W)===V)return;const i=this._$AH,s=t===W&&i!==W||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,a=t!==W&&(i===W||s);s&&this.element.removeEventListener(this.name,this,i),a&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class it{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){K(this,t)}}const st=w.litHtmlPolyfillSupport;st?.(J,G),(w.litHtmlVersions??=[]).push("3.3.1");const at=globalThis;class nt extends b{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{const s=i?.renderBefore??e;let a=s._$litPart$;if(void 0===a){const t=i?.renderBefore??null;s._$litPart$=a=new G(e.insertBefore(U(),t),t,void 0,i??{})}return a._$AI(t),a})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return V}}nt._$litElement$=!0,nt.finalized=!0,at.litElementHydrateSupport?.({LitElement:nt});const rt=at.litElementPolyfillSupport;rt?.({LitElement:nt}),(at.litElementVersions??=[]).push("4.2.1");const ot=n`
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
`,ct={washing_machine:"cycle",dishwasher:"cycle",dryer:"cycle",oven:"cycle",water_heater:"cycle",coffee_maker:"cycle",monitor:"session",nas:"session",printer_3d:"session",vmc:"session",generic:"cycle"},lt={default_tab:"today",show_trends:!0,show_efficiency:!0,chart_type:"bar",theme:"auto"},dt="today",ht="week",pt="month",ut=3e4;function gt(t,e){const i=function(t,e){if(!t||!e)return null;const i=t.states[e];return i?i.state:null}(t,e);if(null===i||"unknown"===i||"unavailable"===i)return null;const s=parseFloat(i);return isNaN(s)?null:s}function vt(t,e=!1){if(!t||t<0)return"0s";const i=Math.floor(t/3600),s=Math.floor(t%3600/60),a=Math.floor(t%60),n=[];return i>0&&n.push(`${i}h`),s>0&&n.push(`${s}m`),!e&&a>0&&0===i&&n.push(`${a}s`),n.length>0?n.join(" "):"0s"}function ft(t,e=2){if(!t||t<0)return"0 kWh";if(t<1){return`${Math.round(1e3*t)} Wh`}return`${t.toFixed(e)} kWh`}function _t(t,e="€",i=2){return!t||t<0?`0.00 ${e}`:`${t.toFixed(i)} ${e}`}function yt(t,e=0){return t||0===t?t.toLocaleString(void 0,{minimumFractionDigits:e,maximumFractionDigits:e}):"0"}customElements.define("smart-appliance-stats-card-editor",class extends nt{static get properties(){return{hass:{type:Object},config:{type:Object}}}setConfig(t){this.config=t}_valueChanged(t){if(!this.config||!this.hass)return;const e=t.target,i="checkbox"===e.type?e.checked:e.value;if(this.config[e.configValue]===i)return;!function(t,e,i={}){const s=new Event(e,{bubbles:!0,composed:!0,cancelable:!1});s.detail=i,t.dispatchEvent(s)}(this,"config-changed",{config:{...this.config,[e.configValue]:i}})}render(){return this.hass&&this.config?I`
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
            placeholder="mdi:chart-box"
          ></ha-icon-picker>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <div class="config-label">Default tab</div>
          <ha-select
            .value=${this.config.default_tab||"today"}
            .configValue=${"default_tab"}
            @selected=${this._valueChanged}
          >
            <mwc-list-item value="today">Today</mwc-list-item>
            <mwc-list-item value="week">Week</mwc-list-item>
            <mwc-list-item value="month">Month</mwc-list-item>
          </ha-select>
          <div class="config-hint">Initial tab to display when card loads</div>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <ha-formfield label="Show trend indicators">
            <ha-switch
              .checked=${!1!==this.config.show_trends}
              .configValue=${"show_trends"}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Display arrows and percentages for trends</div>
        </div>

        <div class="config-section">
          <ha-formfield label="Show efficiency metrics">
            <ha-switch
              .checked=${!1!==this.config.show_efficiency}
              .configValue=${"show_efficiency"}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Show average cost, energy, and duration per cycle</div>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <div class="config-label">Chart type</div>
          <ha-select
            .value=${this.config.chart_type||"bar"}
            .configValue=${"chart_type"}
            @selected=${this._valueChanged}
          >
            <mwc-list-item value="bar">Bar chart</mwc-list-item>
            <mwc-list-item value="line">Line chart</mwc-list-item>
          </ha-select>
          <div class="config-hint">Type of chart for historical data (future feature)</div>
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
    `:I``}static get styles(){return n`
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
    `}});customElements.define("smart-appliance-stats-card",class extends nt{static get properties(){return{hass:{type:Object},config:{type:Object},_entities:{type:Object},_applianceType:{type:String},_terminology:{type:String},_activeTab:{type:String},_updateInterval:{type:Number}}}static getConfigElement(){return document.createElement("smart-appliance-stats-card-editor")}static getStubConfig(){return{entity:"sensor.washing_machine_state",default_tab:"today",show_trends:!0,show_efficiency:!0,chart_type:"bar",theme:"auto"}}constructor(){super(),this._entities=null,this._applianceType="generic",this._terminology="cycle",this._activeTab=dt,this._updateInterval=null}setConfig(t){if(!t.entity)throw new Error("You need to define an entity");this.config={...lt,...t},this._activeTab=this.config.default_tab||dt}connectedCallback(){super.connectedCallback(),this._startAutoUpdate()}disconnectedCallback(){super.disconnectedCallback(),this._stopAutoUpdate()}updated(t){var e;super.updated(t),(t.has("hass")||t.has("config"))&&this.hass&&this.config?.entity&&(this._entities=function(t,e){if(!e||!t)return null;const i=e.match(/^sensor\.(.+)_(state|etat)$/);if(!i)return null;const s=i[1],a="etat"===i[2];return{state:e,cycle_duration:a?`sensor.${s}_duree_du_cycle`:`sensor.${s}_cycle_duration`,cycle_energy:a?`sensor.${s}_energie_du_cycle`:`sensor.${s}_cycle_energy`,cycle_cost:a?`sensor.${s}_cout_du_cycle`:`sensor.${s}_cycle_cost`,last_cycle_duration:a?`sensor.${s}_duree_du_dernier_cycle`:`sensor.${s}_last_cycle_duration`,last_cycle_energy:a?`sensor.${s}_energie_du_dernier_cycle`:`sensor.${s}_last_cycle_energy`,last_cycle_cost:a?`sensor.${s}_cout_du_dernier_cycle`:`sensor.${s}_last_cycle_cost`,daily_cycles:a?`sensor.${s}_cycles_du_jour`:`sensor.${s}_daily_cycles`,daily_cost:a?`sensor.${s}_cout_du_jour`:`sensor.${s}_daily_cost`,monthly_cost:a?`sensor.${s}_cout_du_mois`:`sensor.${s}_monthly_cost`,daily_energy:a?`sensor.${s}_energie_du_jour`:`sensor.${s}_daily_energy`,monthly_energy:a?`sensor.${s}_energie_du_mois`:`sensor.${s}_monthly_energy`,running:a?`binary_sensor.${s}_en_marche`:`binary_sensor.${s}_running`,duration_alert:a?`binary_sensor.${s}_alerte_duree`:`binary_sensor.${s}_duration_alert`,unplugged:a?`binary_sensor.${s}_debranche`:`binary_sensor.${s}_unplugged`,monitoring:a?`switch.${s}_surveillance`:`switch.${s}_monitoring`,notifications:`switch.${s}_notifications`,notify_started:a?`switch.${s}_notification_cycle_demarre`:`switch.${s}_notify_cycle_started`,notify_finished:a?`switch.${s}_notification_cycle_termine`:`switch.${s}_notify_cycle_finished`,notify_alert:a?`switch.${s}_notification_alerte_duree`:`switch.${s}_notify_alert_duration`,notify_unplugged:a?`switch.${s}_notification_debranche`:`switch.${s}_notify_unplugged`,reset_stats:a?`button.${s}_reinitialiser_les_statistiques`:`button.${s}_reset_statistics`}}(this.hass,this.config.entity),this._applianceType=function(t,e){if(!t||!e)return"generic";const i=t.states[e];if(!i)return"generic";const s=i.attributes?.appliance_type;if(s)return s;const a=e.toLowerCase();return a.includes("washing")?"washing_machine":a.includes("dishwasher")?"dishwasher":a.includes("dryer")?"dryer":a.includes("oven")?"oven":a.includes("water")&&a.includes("heater")?"water_heater":a.includes("coffee")?"coffee_maker":a.includes("monitor")||a.includes("screen")?"monitor":a.includes("nas")?"nas":a.includes("printer")&&a.includes("3d")?"printer_3d":a.includes("vmc")||a.includes("ventilation")?"vmc":"generic"}(this.hass,this.config.entity),this._terminology=(e=this._applianceType,ct[e]||"cycle"))}_startAutoUpdate(){this._stopAutoUpdate(),this._updateInterval=setInterval(()=>{this.requestUpdate()},ut)}_stopAutoUpdate(){this._updateInterval&&(clearInterval(this._updateInterval),this._updateInterval=null)}_handleTabClick(t){this._activeTab=t,this.requestUpdate()}_getDailyCycles(){return this._entities&&gt(this.hass,this._entities.daily_cycles)||0}_getDailyCost(){return this._entities&&gt(this.hass,this._entities.daily_cost)||0}_getMonthlyCost(){return this._entities&&gt(this.hass,this._entities.monthly_cost)||0}_getLastCycleDuration(){return this._entities&&gt(this.hass,this._entities.last_cycle_duration)||0}_getLastCycleEnergy(){return this._entities&&gt(this.hass,this._entities.last_cycle_energy)||0}_getLastCycleCost(){return this._entities&&gt(this.hass,this._entities.last_cycle_cost)||0}_renderTabs(){return I`
      <div class="tabs">
        <button
          class="tab ${this._activeTab===dt?"active":""}"
          @click=${()=>this._handleTabClick(dt)}
        >
          <ha-icon icon="mdi:calendar-today"></ha-icon>
          Today
        </button>
        <button
          class="tab ${this._activeTab===ht?"active":""}"
          @click=${()=>this._handleTabClick(ht)}
        >
          <ha-icon icon="mdi:calendar-week"></ha-icon>
          Week
        </button>
        <button
          class="tab ${this._activeTab===pt?"active":""}"
          @click=${()=>this._handleTabClick(pt)}
        >
          <ha-icon icon="mdi:calendar-month"></ha-icon>
          Month
        </button>
      </div>
    `}_renderTodayView(){const t=this._getDailyCycles(),e=this._getDailyCost(),i=this._getLastCycleEnergy(),s=this._getLastCycleDuration(),a=function(t,e){if(!e||0===e)return{direction:"stable",percentage:0};const i=(t-e)/e*100;let s="stable";return i>10?s="up":i<-10&&(s="down"),{direction:s,percentage:i}}(t,Math.max(0,t-1));return I`
      <div class="stats-view fade-in">
        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:counter"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">${this._terminology}s</div>
            <div class="stat-value">${yt(t,0)}</div>
            ${this.config.show_trends?I`
              <div class="stat-trend ${a.direction}">
                ${this._renderTrendIcon(a.direction)}
                ${function(t,e=!0){return t||0===t?`${e&&t>0?"+":""}${Math.round(t)}%`:"0%"}(a.percentage)}
              </div>
            `:""}
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:lightning-bolt"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Energy</div>
            <div class="stat-value">${ft(i*t)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:currency-eur"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Cost</div>
            <div class="stat-value">${_t(e)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:timer"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Avg Duration</div>
            <div class="stat-value">${vt(s,!0)}</div>
          </div>
        </div>
      </div>
    `}_renderWeekView(){const t=7*this._getDailyCycles(),e=7*this._getDailyCost(),i=this._getLastCycleEnergy()*t;return I`
      <div class="stats-view fade-in">
        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:counter"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total ${this._terminology}s</div>
            <div class="stat-value">${yt(t,0)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:lightning-bolt"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total Energy</div>
            <div class="stat-value">${ft(i)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:currency-eur"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total Cost</div>
            <div class="stat-value">${_t(e)}</div>
          </div>
        </div>

        <div class="info-message">
          <ha-icon icon="mdi:information"></ha-icon>
          Weekly statistics require history data
        </div>
      </div>
    `}_renderMonthView(){const t=this._getMonthlyCost(),e=30*this._getDailyCycles(),i=this._getLastCycleEnergy()*e;return I`
      <div class="stats-view fade-in">
        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:counter"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total ${this._terminology}s</div>
            <div class="stat-value">${yt(e,0)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:lightning-bolt"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total Energy</div>
            <div class="stat-value">${ft(i)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:currency-eur"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Monthly Cost</div>
            <div class="stat-value">${_t(t)}</div>
          </div>
        </div>

        <div class="info-message">
          <ha-icon icon="mdi:information"></ha-icon>
          Monthly statistics require history data
        </div>
      </div>
    `}_renderTrendIcon(t){switch(t){case"up":return I`<ha-icon icon="mdi:arrow-up" class="trend-up"></ha-icon>`;case"down":return I`<ha-icon icon="mdi:arrow-down" class="trend-down"></ha-icon>`;default:return I`<ha-icon icon="mdi:arrow-right" class="trend-stable"></ha-icon>`}}_renderEfficiency(){if(!this.config.show_efficiency)return I``;const t=this._getLastCycleCost(),e=this._getLastCycleEnergy(),i=this._getLastCycleDuration();return I`
      <div class="divider"></div>
      <div class="efficiency-section">
        <h3 class="section-title">
          <ha-icon icon="mdi:gauge"></ha-icon>
          Efficiency Metrics
        </h3>
        <div class="efficiency-grid">
          <div class="efficiency-item">
            <span class="efficiency-label">Avg Cost/${this._terminology}</span>
            <span class="efficiency-value">${_t(t)}</span>
          </div>
          <div class="efficiency-item">
            <span class="efficiency-label">Avg Energy/${this._terminology}</span>
            <span class="efficiency-value">${ft(e)}</span>
          </div>
          <div class="efficiency-item">
            <span class="efficiency-label">Avg Duration</span>
            <span class="efficiency-value">${vt(i,!0)}</span>
          </div>
        </div>
      </div>
    `}render(){if(!this.hass||!this.config)return I`<div class="loading">Loading...</div>`;if(!this._entities)return I`
        <ha-card>
          <div class="card">
            <div class="alert-container alert-error">
              <ha-icon icon="mdi:alert-circle"></ha-icon>
              <span>Entity not found: ${this.config.entity}</span>
            </div>
          </div>
        </ha-card>
      `;const t=this.config.name||this.hass.states[this.config.entity]?.attributes?.friendly_name+" Statistics"||"Appliance Statistics",e=this.config.icon||"mdi:chart-box";return I`
      <ha-card>
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">
              <ha-icon icon="${e}"></ha-icon>
              ${t}
            </h2>
          </div>

          ${this._renderTabs()}

          ${this._activeTab===dt?this._renderTodayView():""}
          ${this._activeTab===ht?this._renderWeekView():""}
          ${this._activeTab===pt?this._renderMonthView():""}

          ${this._renderEfficiency()}
        </div>
      </ha-card>
    `}static get styles(){return[ot,n`
        :host {
          display: block;
        }

        ha-card {
          height: 100%;
        }

        .tabs {
          display: flex;
          gap: var(--sac-spacing-sm);
          margin-bottom: var(--sac-spacing);
          border-bottom: 2px solid var(--sac-divider-color);
        }

        .tab {
          flex: 1;
          background: none;
          border: none;
          border-bottom: 2px solid transparent;
          padding: var(--sac-spacing-sm);
          cursor: pointer;
          color: var(--sac-text-secondary);
          font-size: 14px;
          font-weight: 500;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
          transition: all var(--sac-transition-fast);
          margin-bottom: -2px;
        }

        .tab:hover {
          color: var(--sac-text-primary);
          background-color: rgba(0, 0, 0, 0.05);
        }

        .tab.active {
          color: var(--sac-primary-color);
          border-bottom-color: var(--sac-primary-color);
        }

        .stats-view {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: var(--sac-spacing);
        }

        .stat-card {
          background: rgba(0, 0, 0, 0.02);
          border-radius: 8px;
          padding: var(--sac-spacing);
          display: flex;
          gap: var(--sac-spacing-sm);
          align-items: flex-start;
        }

        .stat-icon {
          width: 40px;
          height: 40px;
          background: var(--sac-primary-color);
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }

        .stat-icon ha-icon {
          --mdc-icon-size: 24px;
          color: white;
        }

        .stat-content {
          flex: 1;
          min-width: 0;
        }

        .stat-label {
          font-size: 12px;
          color: var(--sac-text-secondary);
          margin-bottom: 4px;
        }

        .stat-value {
          font-size: 20px;
          font-weight: 600;
          color: var(--sac-text-primary);
        }

        .stat-trend {
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 4px;
          margin-top: 4px;
        }

        .stat-trend.up {
          color: var(--sac-state-error);
        }

        .stat-trend.down {
          color: var(--sac-state-running);
        }

        .stat-trend.stable {
          color: var(--sac-text-secondary);
        }

        .trend-up,
        .trend-down,
        .trend-stable {
          --mdc-icon-size: 16px;
        }

        .section-title {
          font-size: 16px;
          font-weight: 500;
          color: var(--sac-text-primary);
          margin: 0 0 var(--sac-spacing-sm) 0;
          display: flex;
          align-items: center;
          gap: var(--sac-spacing-sm);
        }

        .efficiency-section {
          margin-top: var(--sac-spacing);
        }

        .efficiency-grid {
          display: grid;
          gap: var(--sac-spacing-sm);
        }

        .efficiency-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: var(--sac-spacing-sm);
          background: rgba(0, 0, 0, 0.02);
          border-radius: 6px;
        }

        .efficiency-label {
          font-size: 14px;
          color: var(--sac-text-secondary);
        }

        .efficiency-value {
          font-size: 14px;
          font-weight: 500;
          color: var(--sac-text-primary);
        }

        .info-message {
          grid-column: 1 / -1;
          padding: var(--sac-spacing-sm);
          background: rgba(33, 150, 243, 0.1);
          border-radius: 6px;
          color: var(--sac-text-secondary);
          font-size: 13px;
          display: flex;
          align-items: center;
          gap: var(--sac-spacing-sm);
        }

        @media (max-width: 480px) {
          .stats-view {
            grid-template-columns: 1fr;
          }

          .tab {
            font-size: 12px;
            padding: 6px;
          }

          .stat-value {
            font-size: 18px;
          }
        }
      `]}getCardSize(){return 5}}),window.customCards=window.customCards||[],window.customCards.push({type:"smart-appliance-stats-card",name:"Smart Appliance Stats Card",description:"Comprehensive statistics display with tabbed interface",preview:!0,documentationURL:"https://github.com/legaetan/ha-smart_appliance_monitor/wiki"});

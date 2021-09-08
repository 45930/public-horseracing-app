(this.webpackJsonpclient=this.webpackJsonpclient||[]).push([[0],{165:function(e,a){},196:function(e,a,t){e.exports=t(342)},342:function(e,a,t){"use strict";t.r(a);var n=t(0),r=t.n(n),c=t(41),s=t.n(c),l=t(21),i=t(44),u=t(167),o=t(19),m=t(46),d=t(34),p=t(35),f=t(63),h=t(36),E=function(e){Object(h.a)(t,e);var a=Object(f.a)(t);function t(){return Object(d.a)(this,t),a.apply(this,arguments)}return Object(p.a)(t,[{key:"render",value:function(){return r.a.createElement("div",{className:"ui segment center aligned"},this.props.label)}}]),t}(r.a.Component),v=function(e){Object(h.a)(t,e);var a=Object(f.a)(t);function t(){return Object(d.a)(this,t),a.apply(this,arguments)}return Object(p.a)(t,[{key:"render",value:function(){return r.a.createElement("div",{className:"ui secondary grey inverted menu"},r.a.createElement(o.b,{className:"item",to:"/"},"Home"),r.a.createElement(o.b,{className:"item",to:"/explore"},"Explore"),r.a.createElement(o.b,{className:"item",to:"/results"},"Results"))}}]),t}(r.a.Component),b={track_code:"Track",race_date:"Date",race_number:"Race #",distance:"Distance",surface:"Surface",program_number:"Program Number",trainer:"Trainer",jockey:"Jockey",owner:"Owner",horse_name:"Horse Name"},k=function(e,a){return r.a.createElement("tr",{key:a.horse_id},e.map((function(e){return function(e,a){var t=function(e,a){switch(e){case"trainer":return"/trainers/".concat(a.trainer_id);case"jockey":return"/jockeys/".concat(a.jockey_id);case"owner":return"/owners/".concat(a.owner_id);case"horse_name":return"/horses/".concat(a.horse_id);case"track_code":return"/tracks/".concat(a.track_code);case"race_number":return"/races/".concat(a.race_id)}}(e,a);return t?r.a.createElement("td",{key:e,"data-label":b[e],className:"cell-highlight"},r.a.createElement(o.b,{className:"rowLink",to:t},a[e])):r.a.createElement("td",{key:e,"data-label":e.name},a[e])}(e,a)})),r.a.createElement("td",{"data-label":"Running Line"},function(e){var a=[];return["first","second","third","fourth","fifth","sixth"].forEach((function(t){var n=t+"_call_position";e[n]&&a.push(r.a.createElement("span",{className:"runningLine",key:t},e[n]))})),a}(a)),r.a.createElement("td",{"data-label":"Final Position"},a.final_position),r.a.createElement("td",{"data-label":"Final Odds"},a.odds))},y=function(e){var a=e.headers,t=e.results.slice(0,100);return 0===t.length?"":r.a.createElement("table",{className:"ui basic table"},r.a.createElement("thead",null,r.a.createElement("tr",null,a.map((function(e){return r.a.createElement("th",{key:e},b[e])})),r.a.createElement("th",null,"Running Line"),r.a.createElement("th",null,"Final Position"),r.a.createElement("th",null,"Final Odds"))),r.a.createElement("tbody",null,t.map((function(e){return k(a,e)}))))};y.defaultProps={headers:[],results:[]};var N=y,w=function(e){var a=e.title,t=e.data;return 0===t.length?"":r.a.createElement("table",{className:"ui basic table"},r.a.createElement("thead",null,r.a.createElement("tr",{className:"ui center aligned"},r.a.createElement("th",{colSpan:"3"},a," Win %"))),r.a.createElement("thead",null,r.a.createElement("tr",null,r.a.createElement("th",null,a),r.a.createElement("th",null,"Starts"),r.a.createElement("th",null,"Wins"))),r.a.createElement("tbody",null,t.map((function(e){return r.a.createElement("tr",null,function(e,a){switch(e){case"Jockey":return r.a.createElement("td",{key:a.id,className:"cell-highlight"},r.a.createElement(o.b,{className:"rowLink",to:"/jockeys/".concat(a.id)},a.feature_name));case"Trainer":return r.a.createElement("td",{key:a.id,className:"cell-highlight"},r.a.createElement(o.b,{className:"rowLink",to:"/trainers/".concat(a.id)},a.feature_name));case"Owner":return r.a.createElement("td",{key:a.id,className:"cell-highlight"},r.a.createElement(o.b,{className:"rowLink",to:"/owners/".concat(a.id)},a.feature_name));default:return r.a.createElement("td",null,a.feature_name)}}(a,e),r.a.createElement("td",null,e.starts),r.a.createElement("td",null,e.wins+0," (",Math.round(100*e.wins/e.starts,2),"%)"))}))))};w.defaultProps={title:"",data:[]};var _,j=w,g=t(10),O=t.n(g),x=t(25),C=t(169),R=t.n(C).a.create({baseURL:"http://0.0.0.0:8000/api/"}),T=function(e){return function(){var a=Object(x.a)(O.a.mark((function a(t){var n;return O.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,R.post("/results/",e);case 2:n=a.sent,t({type:"QUERY_RESULTS",payload:n.data});case 4:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()},S=(t(71),function(e){Object(h.a)(t,e);var a=Object(f.a)(t);function t(){return Object(d.a)(this,t),a.apply(this,arguments)}return Object(p.a)(t,[{key:"componentDidMount",value:function(){return this.props.fetchCards()}},{key:"renderedCard",value:function(e){var a=e.track_code.toUpperCase()+" - "+e.date;return r.a.createElement("div",{className:"six wide computer eight wide tablet column",key:a},r.a.createElement("div",{className:"race"},r.a.createElement("div",{className:"ui header center aligned"},a),r.a.createElement("div",{className:"ui content"},r.a.createElement("table",{className:"ui compact basic table"},r.a.createElement("thead",null,r.a.createElement("tr",null,r.a.createElement("th",null,"Race"),r.a.createElement("th",null,"Distance"),r.a.createElement("th",null,"Surface"),r.a.createElement("th",null,"Class"),r.a.createElement("th",null,"Purse"))),r.a.createElement("tbody",null,e.races.map((function(e){return r.a.createElement("tr",{key:e.id,className:"row-highlight"},r.a.createElement("td",{"data-label":"Race"},r.a.createElement(o.b,{className:"rowLink",to:"/races/".concat(e.id)},e.race_number)),r.a.createElement("td",{"data-label":"Distance"},r.a.createElement(o.b,{className:"rowLink",to:"/races/".concat(e.id)},e.distance)),r.a.createElement("td",{"data-label":"Surface"},r.a.createElement(o.b,{className:"rowLink",to:"/races/".concat(e.id)},e.surface)),r.a.createElement("td",{"data-label":"Class"},r.a.createElement(o.b,{className:"rowLink",to:"/races/".concat(e.id)},e.classification)),r.a.createElement("td",{"data-label":"Purse"},r.a.createElement(o.b,{className:"rowLink",to:"/races/".concat(e.id)},e.purse)))})))))))}},{key:"renderedCards",value:function(){var e=this;return r.a.createElement("div",{className:"ui row scroll"},this.props.cards.map((function(a){return e.renderedCard(a)})))}},{key:"renderedConnections",value:function(){return r.a.createElement("div",{className:"ui three column row"},r.a.createElement("div",{className:"column"},r.a.createElement("div",{className:"ui card"},r.a.createElement("div",{className:"ui header"},"Trainers"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"))),r.a.createElement("div",{className:"column"},r.a.createElement("div",{className:"ui card"},r.a.createElement("div",{className:"ui header"},"Jockeys"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"))),r.a.createElement("div",{className:"column"},r.a.createElement("div",{className:"ui card"},r.a.createElement("div",{className:"ui header"},"Combo"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"),r.a.createElement("div",{className:"content"},"line"))))}},{key:"render",value:function(){return r.a.createElement("div",null,r.a.createElement("div",{className:"ui relaxed grid"},r.a.createElement("div",{className:"ui row"},r.a.createElement("div",{className:"left floated eight wide column"},r.a.createElement("h2",{className:"ui header"},"Recent Cards")),r.a.createElement("span",{className:"four wide column"}),r.a.createElement("div",{className:"right floated four wide column"},r.a.createElement(E,{label:"Select Tracks"}))),this.renderedCards()),r.a.createElement("div",{className:"ui grid"},r.a.createElement("div",{className:"ui row"},r.a.createElement("div",{className:"eight wide column"},r.a.createElement("h2",{className:"ui header"},"Hot Connections")),r.a.createElement("div",{className:"four wide column"},r.a.createElement(E,{label:"Select Date Range"})),r.a.createElement("div",{className:"four wide column"},r.a.createElement(E,{label:"Select Tracks"}))),this.renderedConnections()))}}]),t}(r.a.Component)),F=Object(l.b)((function(e){return{cards:e.backend.cards}}),{fetchCards:function(){return function(){var e=Object(x.a)(O.a.mark((function e(a){var t;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,R.get("/cards/");case 2:t=e.sent,a({type:"FETCH_CARDS",payload:t.data});case 4:case"end":return e.stop()}}),e)})));return function(a){return e.apply(this,arguments)}}()}})(S),D=t(186),I=t(28),H=t(29),A=t(90),J=t(30),q=t(31),M=t(352),L=t(351),W=function(e){Object(q.a)(t,e);var a=Object(J.a)(t);function t(e){var n;return Object(I.a)(this,t),(n=a.call(this,e)).state={filter:{date:{},track:[],trainer:[],jockey:[],surface:[],distance:{}}},n.handleSubmit=n.handleSubmit.bind(Object(A.a)(n)),n}return Object(H.a)(t,[{key:"componentWillMount",value:function(){this.props.queryResults(this.buildFilter()),this.props.indexJockeys(),this.props.indexTrainers(),this.props.indexTracks()}},{key:"handleFilterEvent",value:function(e,a){console.log(e),console.log(a);var t,n,r=this.state.filter,c=e.split(">"),s=r,l=Object(D.a)(c);try{for(l.s();!(n=l.n()).done;){var i=n.value;t&&(s=s[t]),t=i}}catch(u){l.e(u)}finally{l.f()}s[t]=a.target.value,console.log(r),this.setState({filter:r})}},{key:"handleDropdownChange",value:function(e,a,t){var n=t.value,r=this.state.filter;r[e]=n,this.setState({filter:r})}},{key:"handleSubmit",value:function(e){e.preventDefault(),this.props.queryResults(this.buildFilter())}},{key:"handleMultiSelect",value:function(e,a){for(var t=a.target.options,n=[],r=0,c=t.length;r<c;r++)t[r].selected&&n.push(t[r].value);this.setState({value:n})}},{key:"buildFilter",value:function(){var e=this.state.filter,a=[];return Object.keys(e.date).length>0&&(void 0!==e.date.min&&a.push({field:"date",operator:"gte",arguments:[e.date.min]}),void 0!==e.date.max&&a.push({field:"date",operator:"lte",arguments:[e.date.max]})),e.track.length>0&&a.push({field:"track_id",operator:"in",arguments:e.track}),e.trainer.length>0&&a.push({field:"trainer_id",operator:"in",arguments:e.trainer}),e.jockey.length>0&&a.push({field:"jockey_id",operator:"in",arguments:e.jockey}),e.surface.length>0&&a.push({field:"surface",operator:"in",arguments:e.surface}),Object.keys(e.distance).length>0&&(void 0!==e.distance.min&&a.push({field:"distance",operator:"gte",arguments:[e.distance.min]}),void 0!==e.distance.max&&a.push({field:"distance",operator:"lte",arguments:[e.distance.max]})),a}},{key:"renderedFilters",value:function(){return r.a.createElement("div",{className:"ui form"},r.a.createElement("div",{className:"ui grid row"},r.a.createElement("div",{className:"ui five wide column"},r.a.createElement("div",{className:"field"},r.a.createElement("label",null,"Start Date:",r.a.createElement("input",{type:"date",value:this.state.filter.date.min,onChange:this.handleFilterEvent.bind(this,"date>min")})))),r.a.createElement("div",{className:"ui one wide column"}),r.a.createElement("div",{className:"ui five wide column"},r.a.createElement("div",{className:"field"},r.a.createElement("label",null,"End Date:",r.a.createElement("input",{type:"date",value:this.state.filter.date.max,onChange:this.handleFilterEvent.bind(this,"date>max")}))))),r.a.createElement("div",{className:"ui grid row"},r.a.createElement("div",{className:"ui four wide column"},r.a.createElement("div",{className:"field"},r.a.createElement("label",null,"Tracks"),r.a.createElement(M.a,{placeholder:"Select Tracks",fluid:!0,search:!0,selection:!0,multiple:!0,options:this.props.trackIndex.map((function(e){return{key:e.id,value:e.id,text:e.code}})),onChange:this.handleDropdownChange.bind(this,"track")}))),r.a.createElement("div",{className:"ui four wide column"},r.a.createElement("div",{className:"field"},r.a.createElement("label",null,"Trainers"),r.a.createElement(M.a,{placeholder:"Select Trainer",fluid:!0,search:!0,selection:!0,multiple:!0,options:this.props.trainerIndex.map((function(e){return{key:e.id,value:e.id,text:e.full_name}})),onChange:this.handleDropdownChange.bind(this,"trainer")}))),r.a.createElement("div",{className:"ui four wide column"},r.a.createElement("div",{className:"field"},r.a.createElement("label",null,"Jockeys"),r.a.createElement(M.a,{placeholder:"Select Jockey",fluid:!0,search:!0,selection:!0,multiple:!0,options:this.props.jockeyIndex.map((function(e){return{key:e.id,value:e.id,text:e.full_name}})),onChange:this.handleDropdownChange.bind(this,"jockey")}))),r.a.createElement("div",{className:"ui four wide column"},r.a.createElement("div",{className:"field"},r.a.createElement("label",null,"Surface"),r.a.createElement(M.a,{placeholder:"Select Surface",fluid:!0,search:!0,selection:!0,multiple:!0,options:[{key:"d",value:"d",text:"Dirt"},{key:"t",value:"t",text:"Turf"}],onChange:this.handleDropdownChange.bind(this,"surface")})))),r.a.createElement("div",{className:"ui grid row"},r.a.createElement("div",{className:"ui four wide column"},r.a.createElement("div",{className:"field"},r.a.createElement("label",null,"Min Distance",r.a.createElement("input",{type:"number",value:this.state.filter.distance.min,onChange:this.handleFilterEvent.bind(this,"distance>min")})))),r.a.createElement("div",{className:"ui four wide column"},r.a.createElement("div",{className:"field"},r.a.createElement("label",null,"Max Distance",r.a.createElement("input",{type:"number",value:this.state.filter.distance.max,onChange:this.handleFilterEvent.bind(this,"distance>max")}))))),r.a.createElement("div",{className:"ui grid row"},r.a.createElement("div",{className:"column"},r.a.createElement("button",{onClick:this.handleSubmit},"Update Filter"))),r.a.createElement("div",{className:"ui divider"}))}},{key:"renderedStats",value:function(){var e,a,t,n=this.props.results,c=0,s=n.length,l=[],i=[];return this.props.results.forEach((function(e){l.push(e.odds),1===e.final_position&&(c+=1,i.push(e.odds))})),s>0&&(e=(Object(L.a)(l)/100).toFixed(2),t=(((a=c>0?(Object(L.a)(i)/100).toFixed(2):0)+1)*c*2/s).toFixed(2)),r.a.createElement("div",{className:"ui grid row"},r.a.createElement("div",{className:"ui three wide column"},r.a.createElement("div",{className:"ui segment"},r.a.createElement("div",{className:"content"},"Starts: ",s))),r.a.createElement("div",{className:"ui two wide column"},r.a.createElement("div",{className:"ui segment"},r.a.createElement("div",{className:"content"},"Wins: ",c))),r.a.createElement("div",{className:"ui four wide column"},r.a.createElement("div",{className:"ui segment"},r.a.createElement("div",{className:"content"},"Average Odds: ",e))),r.a.createElement("div",{className:"ui four wide column"},r.a.createElement("div",{className:"ui segment"},r.a.createElement("div",{className:"content"},"Avereage Winning Odds: ",a))),r.a.createElement("div",{className:"ui three wide column"},r.a.createElement("div",{className:"ui segment"},r.a.createElement("div",{className:"content"},"$2 ROI: ",t))))}},{key:"render",value:function(){return r.a.createElement("div",{className:"ui container"},this.renderedFilters(),this.renderedStats(),r.a.createElement("div",{className:"ui divider"}),r.a.createElement("div",null,r.a.createElement("h2",{className:"ui header"},"Results with Filter"),r.a.createElement(N,{headers:["track_code","race_date","distance","surface","horse_name","trainer","jockey"],results:this.props.results})))}}]),t}(r.a.Component),P=Object(l.b)((function(e){return{results:e.backend.results,jockeyIndex:e.backend.jockeyIndex,trainerIndex:e.backend.trainerIndex,trackIndex:e.backend.trackIndex}}),{queryResults:T,indexJockeys:function(){return function(){var e=Object(x.a)(O.a.mark((function e(a){var t;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,R.get("/jockeys/");case 2:t=e.sent,a({type:"INDEX_JOCKEYS",payload:t.data});case 4:case"end":return e.stop()}}),e)})));return function(a){return e.apply(this,arguments)}}()},indexTrainers:function(){return function(){var e=Object(x.a)(O.a.mark((function e(a){var t;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,R.get("/trainers/");case 2:t=e.sent,a({type:"INDEX_TRAINERS",payload:t.data});case 4:case"end":return e.stop()}}),e)})));return function(a){return e.apply(this,arguments)}}()},indexTracks:function(){return function(){var e=Object(x.a)(O.a.mark((function e(a){var t;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,R.get("/tracks/");case 2:t=e.sent,a({type:"INDEX_TRACKS",payload:t.data});case 4:case"end":return e.stop()}}),e)})));return function(a){return e.apply(this,arguments)}}()}})(W),U=(t(165),function(e){Object(q.a)(t,e);var a=Object(J.a)(t);function t(){return Object(I.a)(this,t),a.apply(this,arguments)}return Object(H.a)(t,[{key:"componentDidMount",value:function(){var e=this.props.match.params.id;this.props.fetchRace(e),this.props.queryResults([{field:"race_id",operator:"eq",arguments:[e]}])}},{key:"renderedClass",value:function(e){var a;switch(e){case"mcl":a="Maiden Claiming";break;case"gstk":a="Graded Stakes";break;case"an2l":a="Allowance, Non-Winners of Two";break;case"clm":a="Claimimg";break;case"ocln":a="Allowance Optional Claiming Non-Winners of One";break;case"stk":a="Overnight Stakes";break;case"soc":a="Starter Allowance Optional Claiming";break;case"clmn":a="Claiming Non-Winners of One";break;case"str":a="Starter Allowance";break;case"msw":a="Maiden Special Weight";break;case"aoc":a="Allowance Optional Claiming";break;case"alw":a="Allowance";break;case"an3l":a="Allowance Non-Winners of Three";break;case"mdn":a="Maiden";break;default:a=e}return a}},{key:"restrictionText",value:function(e,a,t){var n,r,c;switch(e){case"31":n="Three year olds and up";break;case"21":n="Two year olds and up";break;case"3":n="Three year olds";break;case"2":n="Two year olds";break;default:n=e}switch(a){case"o":r=", open company";break;case"m":r=", fillies and mares";break;case"f":r=", fillies";break;default:r=", ".concat(a)}return c=t?", statebred":"",n.concat(r,c)}},{key:"renderedClaimPrice",value:function(){var e=this.props.race;return e.claim_price?r.a.createElement("div",null,"Claim Price: ",e.claim_price):""}},{key:"renderedRaceInfo",value:function(){var e=this.props.race;return void 0===e.track_code?null:r.a.createElement("div",{className:"ui segment"},r.a.createElement("div",null,r.a.createElement("h2",{className:"ui header center aligned"},e.track_code.toUpperCase()+" - "+e.date+" Race "+e.race_number)),r.a.createElement("div",null,r.a.createElement("div",null,"Class: ",this.renderedClass(e.classification)),r.a.createElement("div",null,"Purse: ",e.purse),this.renderedClaimPrice(),r.a.createElement("div",null,"Restrictions:"," ",this.restrictionText(e.age_restrictions,e.sex_restrictions,e.is_state_bred))))}},{key:"render",value:function(){return r.a.createElement("div",null,r.a.createElement("div",null,this.renderedRaceInfo()),r.a.createElement(N,{headers:["program_number","horse_name","trainer","jockey","owner"],results:this.props.results}))}}]),t}(r.a.Component)),X=Object(l.b)((function(e){return{race:e.backend.race,results:e.backend.results}}),{fetchRace:function(e){return function(){var a=Object(x.a)(O.a.mark((function a(t){var n;return O.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,R.get("/races/".concat(e));case 2:n=a.sent,t({type:"FETCH_RACE",payload:n.data});case 4:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()},queryResults:T})(U),K=function(e){Object(q.a)(t,e);var a=Object(J.a)(t);function t(){return Object(I.a)(this,t),a.apply(this,arguments)}return Object(H.a)(t,[{key:"componentDidMount",value:function(){var e=this.props.match.params.id;this.props.fetchHorse(e),this.props.queryResults([{field:"horse_id",operator:"eq",arguments:[e]}])}},{key:"render",value:function(){return r.a.createElement("div",null,r.a.createElement("div",null,r.a.createElement("h2",{className:"ui header"},this.props.horse.name)),r.a.createElement(N,{headers:["track_code","race_date","race_number","distance","surface","program_number","trainer","jockey","owner"],results:this.props.results}))}}]),t}(r.a.Component),Y=Object(l.b)((function(e){return{horse:e.backend.horse,results:e.backend.results}}),{fetchHorse:function(e){return function(){var a=Object(x.a)(O.a.mark((function a(t){var n;return O.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,R.get("/horse/".concat(e));case 2:n=a.sent,t({type:"FETCH_HORSE",payload:n.data});case 4:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()},queryResults:T})(K),Q=t(8),G=function(e){Object(q.a)(t,e);var a=Object(J.a)(t);function t(){return Object(I.a)(this,t),a.apply(this,arguments)}return Object(H.a)(t,[{key:"componentDidMount",value:function(){var e=this.props.match.params.id;this.props.fetchTrainer(e),this.props.fetchTrainerStats(e),this.props.queryResults([{field:"trainer_id",operator:"eq",arguments:[e]}])}},{key:"routeText",value:function(e){return 1===e?"Route":"Sprint"}},{key:"winRate",value:function(){var e=0,a=0;return this.props.trainer.surface_stats.forEach((function(t){e+=t.wins,a+=t.starts})),a>0?Math.round(100*e/a,2):0}},{key:"render",value:function(){var e=this;return r.a.createElement("div",null,r.a.createElement("div",{className:"ui grid"},r.a.createElement("div",{className:"ui row"},r.a.createElement("div",{className:"ui six wide column"},r.a.createElement("h2",{className:"ui header left floated"},"Name"),r.a.createElement("div",null,this.props.trainer.full_name)),r.a.createElement("div",{className:"ui six wide column right floated"},r.a.createElement("div",{className:"ui grid row"},r.a.createElement("h2",{className:"ui header left floated"},"Win %"),r.a.createElement("div",{className:"ui right floated content"},this.winRate())))),r.a.createElement("div",{className:"ui four column row"},r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Track",data:this.props.trainer.track_stats.map((function(e){return Object(Q.a)({},e,{feature_name:e.track_code})}))})),r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Jockey",data:this.props.trainer.jockey_stats.map((function(e){return Object(Q.a)({},e,{feature_name:e.full_name})}))})),r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Class",data:this.props.trainer.class_stats.map((function(e){return Object(Q.a)({},e,{feature_name:e.classification})}))})),r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Surface",data:this.props.trainer.surface_stats.map((function(a){return Object(Q.a)({},a,{feature_name:"".concat(a.surface," - ").concat(e.routeText(a.route))})}))})))),r.a.createElement("h2",{className:"ui header"},"Recent Results"),r.a.createElement(N,{headers:["track_code","race_date","race_number","distance","surface","program_number","horse_name","jockey","owner"],results:this.props.results}))}}]),t}(r.a.Component),V=Object(l.b)((function(e){return{trainer:e.backend.trainer,results:e.backend.results}}),{fetchTrainer:function(e){return function(){var a=Object(x.a)(O.a.mark((function a(t){var n;return O.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,R.get("/trainers/".concat(e));case 2:n=a.sent,t({type:"FETCH_TRAINER",payload:n.data});case 4:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()},fetchTrainerStats:function(e){return function(){var a=Object(x.a)(O.a.mark((function a(t){var n;return O.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,R.get("/trainers/stats/".concat(e));case 2:n=a.sent,t({type:"FETCH_TRAINER",payload:n.data});case 4:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()},queryResults:T})(G),$=function(e){Object(q.a)(t,e);var a=Object(J.a)(t);function t(){return Object(I.a)(this,t),a.apply(this,arguments)}return Object(H.a)(t,[{key:"componentDidMount",value:function(){var e=this.props.match.params.id;this.props.fetchJockey(e),this.props.fetchJockeyStats(e),this.props.queryResults([{field:"jockey_id",operator:"eq",arguments:[e]}])}},{key:"routeText",value:function(e){return 1===e?"Route":"Sprint"}},{key:"winRate",value:function(){var e=0,a=0;return this.props.jockey.surface_stats.forEach((function(t){e+=t.wins,a+=t.starts})),a>0?Math.round(100*e/a,2):0}},{key:"render",value:function(){var e=this;return r.a.createElement("div",null,r.a.createElement("div",{className:"ui grid"},r.a.createElement("div",{className:"ui row"},r.a.createElement("div",{className:"ui six wide column"},r.a.createElement("h2",{className:"ui header left floated"},"Name"),r.a.createElement("div",null,this.props.jockey.full_name)),r.a.createElement("div",{className:"ui six wide column right floated"},r.a.createElement("div",{className:"ui grid row"},r.a.createElement("h2",{className:"ui header left floated"},"Win %"),r.a.createElement("div",{className:"ui right floated content"},this.winRate())))),r.a.createElement("div",{className:"ui four column row"},r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Track",data:this.props.jockey.track_stats.map((function(e){return Object(Q.a)({},e,{feature_name:e.track_code})}))})),r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Trainer",data:this.props.jockey.trainer_stats.map((function(e){return Object(Q.a)({},e,{feature_name:e.full_name})}))})),r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Class",data:this.props.jockey.class_stats.map((function(e){return Object(Q.a)({},e,{feature_name:e.classification})}))})),r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Surface",data:this.props.jockey.surface_stats.map((function(a){return Object(Q.a)({},a,{feature_name:"".concat(a.surface," - ").concat(e.routeText(a.route))})}))})))),r.a.createElement(N,{headers:["track_code","race_date","race_number","distance","surface","program_number","horse_name","trainer","owner"],results:this.props.results}))}}]),t}(r.a.Component),z=Object(l.b)((function(e){return{jockey:e.backend.jockey,results:e.backend.results}}),{fetchJockey:function(e){return function(){var a=Object(x.a)(O.a.mark((function a(t){var n;return O.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,R.get("/jockeys/".concat(e));case 2:n=a.sent,t({type:"FETCH_JOCKEY",payload:n.data});case 4:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()},fetchJockeyStats:function(e){return function(){var a=Object(x.a)(O.a.mark((function a(t){var n;return O.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,R.get("/jockeys/stats/".concat(e));case 2:n=a.sent,t({type:"FETCH_JOCKEY",payload:n.data});case 4:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()},queryResults:T})($),B=function(e){Object(q.a)(t,e);var a=Object(J.a)(t);function t(){return Object(I.a)(this,t),a.apply(this,arguments)}return Object(H.a)(t,[{key:"componentDidMount",value:function(){var e=this.props.match.params.id;this.props.fetchOwner(e),this.props.fetchOwnerStats(e),this.props.queryResults([{field:"owner_id",operator:"eq",arguments:[e]}])}},{key:"routeText",value:function(e){return 1===e?"Route":"Sprint"}},{key:"winRate",value:function(){var e=0,a=0;return this.props.owner.surface_stats.forEach((function(t){e+=t.wins,a+=t.starts})),a>0?Math.round(100*e/a,2):0}},{key:"render",value:function(){var e=this;return r.a.createElement("div",null,r.a.createElement("div",{className:"ui grid"},r.a.createElement("div",{className:"ui row"},r.a.createElement("div",{className:"ui six wide column"},r.a.createElement("h2",{className:"ui header left floated"},"Name"),r.a.createElement("div",null,this.props.owner.full_name)),r.a.createElement("div",{className:"ui six wide column right floated"},r.a.createElement("div",{className:"ui grid row"},r.a.createElement("h2",{className:"ui header left floated"},"Win %"),r.a.createElement("div",{className:"ui right floated content"},this.winRate())))),r.a.createElement("div",{className:"ui four column row"},r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Trainer",data:this.props.owner.trainer_stats.map((function(e){return Object(Q.a)({},e,{feature_name:e.full_name})}))})),r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Jockey",data:this.props.owner.jockey_stats.map((function(e){return Object(Q.a)({},e,{feature_name:e.full_name})}))})),r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Class",data:this.props.owner.class_stats.map((function(e){return Object(Q.a)({},e,{feature_name:e.classification})}))})),r.a.createElement("div",{className:"ui column"},r.a.createElement(j,{title:"Surface",data:this.props.owner.surface_stats.map((function(a){return Object(Q.a)({},a,{feature_name:"".concat(a.surface," - ").concat(e.routeText(a.route))})}))})))),r.a.createElement(N,{headers:["track_code","race_date","race_number","distance","surface","program_number","horse_name","trainer","jockey"],results:this.props.results}))}}]),t}(r.a.Component),Z=Object(l.b)((function(e){return{owner:e.backend.owner,results:e.backend.results}}),{fetchOwner:function(e){return function(){var a=Object(x.a)(O.a.mark((function a(t){var n;return O.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,R.get("/owners/".concat(e));case 2:n=a.sent,t({type:"FETCH_OWNER",payload:n.data});case 4:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()},fetchOwnerStats:function(e){return function(){var a=Object(x.a)(O.a.mark((function a(t){var n;return O.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,R.get("/owners/stats/".concat(e));case 2:n=a.sent,t({type:"FETCH_OWNER",payload:n.data});case 4:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()},queryResults:T})(B),ee=function(){return r.a.createElement("div",{className:"ui container"},r.a.createElement(o.a,null,r.a.createElement(v,null),r.a.createElement("div",null,r.a.createElement(m.a,{path:"/",exact:!0,component:F}),r.a.createElement(m.a,{path:"/races/:id",exact:!0,component:X}),r.a.createElement(m.a,{path:"/horses/:id",exact:!0,component:Y}),r.a.createElement(m.a,{path:"/trainers/:id",exact:!0,component:V}),r.a.createElement(m.a,{path:"/jockeys/:id",exact:!0,component:z}),r.a.createElement(m.a,{path:"/owners/:id",exact:!0,component:Z}),r.a.createElement(m.a,{path:"/explore",exact:!0,component:P}))))},ae=t(70),te=(t(341),_={cards:[],race:{},trainer:{track_stats:[],jockey_stats:[],class_stats:[],surface_stats:[]},jockey:{track_stats:[],trainer_stats:[],class_stats:[],surface_stats:[]},owner:{trainer_stats:[],jockey_stats:[],class_stats:[],surface_stats:[]},results:[],horse:{},trainerIndex:[],jockeyIndex:[]},Object(ae.a)(_,"trainerIndex",[]),Object(ae.a)(_,"trackIndex",[]),_),ne=Object(i.c)({backend:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:te,a=arguments.length>1?arguments[1]:void 0;switch(a.type){case"FETCH_CARDS":return Object(Q.a)({},e,{cards:a.payload});case"FETCH_HORSE":return Object(Q.a)({},e,{horse:a.payload});case"FETCH_RACE":return Object(Q.a)({},e,{race:a.payload});case"FETCH_TRAINER":return Object(Q.a)({},e,{trainer:Object(Q.a)({},e.trainer,{},a.payload)});case"FETCH_JOCKEY":return Object(Q.a)({},e,{jockey:Object(Q.a)({},e.jockey,{},a.payload)});case"FETCH_OWNER":return Object(Q.a)({},e,{owner:Object(Q.a)({},e.owner,{},a.payload)});case"QUERY_RESULTS":return Object(Q.a)({},e,{results:a.payload});case"INDEX_JOCKEYS":return Object(Q.a)({},e,{jockeyIndex:a.payload});case"INDEX_TRAINERS":return Object(Q.a)({},e,{trainerIndex:a.payload});case"INDEX_TRACKS":return Object(Q.a)({},e,{trackIndex:a.payload});default:return e}}}),re=window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__||i.d,ce=Object(i.e)(ne,re(Object(i.a)(u.a)));s.a.render(r.a.createElement(l.a,{store:ce},r.a.createElement(ee,null)),document.querySelector("#root"))},71:function(e,a,t){}},[[196,1,2]]]);
//# sourceMappingURL=main.dfb1f83b.chunk.js.map
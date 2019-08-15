import 'bootstrap/dist/css/bootstrap.css';
import * as d3 from 'd3'
import $ from 'jquery'
import 'bootstrap/dist/css/bootstrap.css';

/* Das Konstruieren der Daten für das Zeichnen der Säulendiagramme der Ergebnisse der Wörterbuchanalyse. */
export const buildDictionaryBarData = (result=undefined, second=false, setState) => {
    setState({loading: true})

    let bar_data = result.map((entry) => {
        return {name: entry.id, Kalt: entry.counters.Kalt, Warm: entry.counters.Warm}
    })
    if(second){
        setState({secondDictionaryBarData: bar_data, loading: false})
    }else{
        setState({dictionaryBarData: bar_data, loading: false})
    }
}

/* Das Konstruieren der Daten für das Zeichnen der Diagramme mit den Ergebnissen der LDA-Analyse. Hier wurde der Code
*  wieder zu großen Teilen aus Scarlett übernommen und nur soweit angepasst, dass die Darstellung in dieser Anwendung
*  korrekt erfolgen konnte. */
export const buildTopicBarData = (entries_object, topics_object, second=false, setState, state) => {
    setState({loading: true})
    var bars_data = {};
    bars_data['topic-datasets'] = {};

    var n_entries = Object.keys(entries_object).length;
    var entry_name_list = new Array(n_entries);
    for (var entry in entries_object){
        entry_name_list[entries_object[entry]['position']] = entry;
    }
    bars_data['entry-names'] = entry_name_list;

    var topic_list = [];
    for (var topic in topics_object){
        topic_list.push(topic);

        var dataset = new Array(n_entries+1).join('0').split('').map(parseInt);
        for (var position in entry_name_list){
            var topic_prob = entries_object[entry_name_list[position]]['topic_probabilities'][topic];
            dataset[position] = topic_prob;
        }
        bars_data['topic-datasets'][topic] = dataset;
    }
    topic_list.sort();
    bars_data['topic-list'] = topic_list;
    if(second){
        setState({secondTopicbarData: bars_data, loading: false}, () => {
            paint_topicbars(true, bars_data, topics_object);
            paint_topicbars(false, state.topicbarData, state.ldaResult['topics']);
        })
    }else{
        setState({topicbarData: bars_data, loading: false}, () => {
            paint_topicbars(false, bars_data, topics_object)
        })
    }
}

/* Das eigentliche Zeichnen der Diagramme in das vorher leer gerenderte Template mithilfe von d3 und jquery. Auch dieser
*  Code stammt im Ursprung aus Scarlett und wurde nur soweit angepasst wie nötig. */
export const paint_topicbars = (second=false, data, topics) => {
    if(second){
        $('#lda-second-topic-bars').empty();
    }else{
        $('#lda-topic-bars').empty();
    }

    var bar_data = data
    var topic_list = bar_data['topic-list'];
    var topic_datasets = bar_data['topic-datasets'];
    var entry_names = bar_data['entry-names'];
    var topics_data = topics;
    var top_words_key = 'top_words';


    var shortNames = entry_names
    shortNames.push('undefined'); //fixes scale issue offset of one

    for (var i in topic_list){
        var topic = topic_list[i];
        var ldaTopicBar;
        if(second){
            ldaTopicBar = $('.lda-second-topic-bar-template').clone();
            ldaTopicBar.toggleClass('lda-second-topic-bar-template lda-second-topic-bar template');
            ldaTopicBar.attr("id", "second" + topic +"_entries_distri");
            ldaTopicBar.find('.lda-second-topic-bar-name').text(topic);
            ldaTopicBar.find('.lda-second-topic-bar-name').attr('title', topics_data[topic][top_words_key].join());
            ldaTopicBar.appendTo('#lda-second-topic-bars');
        }else{
            ldaTopicBar = $('.lda-topic-bar-template').clone();
            ldaTopicBar.toggleClass('lda-topic-bar-template lda-topic-bar template');
            ldaTopicBar.attr("id", topic +"_entries_distri");
            ldaTopicBar.find('.lda-topic-bar-name').text(topic);
            ldaTopicBar.find('.lda-topic-bar-name').attr('title', topics_data[topic][top_words_key].join());
            ldaTopicBar.appendTo('#lda-topic-bars');
        }

        var w = ldaTopicBar.width();
        var h = 200;
        var barPadding = 1;
        var barHeightPadding = 50;

        var xScale = d3.scale.linear()
            .domain([0, topic_datasets[topic].length])
            .range([0,w]);

        var axeScale = d3.scale.ordinal()
            .domain(shortNames)
            .rangePoints([0, w]);

        var yScale = d3.scale.linear()
            .domain([0, 1])
            .range([0, h-barHeightPadding]);

        var colorScale = d3.scale.linear()
            .domain([0, d3.max(topic_datasets[topic], function(d){
                return d;
            })])
            .range([0, 200]);

        //Create SVG element
        var svg = d3.select("#" + ldaTopicBar.attr("id"))
            .append("svg")
            .attr("width", w)
            .attr("height", h);

        //Append rectangles
        svg.selectAll("rect")
            .data(topic_datasets[topic])
            .enter()
            .append("rect")
            .attr("x", (d, i) => {
                return xScale(i);
            })
            .attr("y", (d) => {
                return h-barHeightPadding - yScale(d);  //Height minus data value
            })
            .attr("width", w / topic_datasets[topic].length - barPadding)
            .attr("height", function(d) {
                return yScale(d);  //Just the data value
            }).attr("fill", function(d) {
            return "rgb(0, " + parseInt(colorScale(d)) + ", 0)";
        });

        //format to percent
        var format2Perc = d3.format(".1%");

        //percentage text
        svg.selectAll("text")
            .data(topic_datasets[topic])
            .enter()
            .append("text").text(function(d) {
            if (d>0.15) return format2Perc(d);
            else return '';
        })
            .attr("x", function(d, i) {
                return i * (w / topic_datasets[topic].length) + (w / topic_datasets[topic].length - barPadding) / 2;
            })
            .attr("y", function(d) {
                return h - barHeightPadding - yScale(d) + 10;
            })
            .attr("font-family", "sans-serif")
            .attr("font-size", "10px")
            .attr("fill", "white")
            .attr("text-anchor", "middle");

        var xAxis = d3.svg.axis()
            .scale(axeScale)
            .orient("bottom")

        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate("+(w / topic_datasets[topic].length - barPadding) / 2+"," + (h - barHeightPadding+2) + ")")
            .call(xAxis);

    }
}
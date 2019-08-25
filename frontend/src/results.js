import React from 'react'
import {Tabs, Tab} from 'material-ui/Tabs'
import {paint_topicbars} from './Helper/charts'
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine,
} from 'recharts';

const Results = (props) => {
    const {state, setState} = props

    // Liefert das Ergebnis der LDA Analyse. Listet die gefundenen Themen mit seinen häufigsten Wörtern auf und
    // zeichnet darunter die Säulendiagramme für die Themen. Die Darstellung wurde aus Scarlett übernommen und auf eine
    // passende Darstellungsweise und Implementierung für diese Anwendung angepasst.
    const FirstLDAResult = (props) => {
        return(
            <div className={props.className}>
                <div style={props.style}>
                    {state.ldaResult && state.ldaResult.topics ? Object.keys(state.ldaResult.topics).map((topic) => {
                        return (
                            <div>
                                {topic}:
                                <ul>
                                    {state.ldaResult.topics[topic].top_words.map((word) => {
                                        return (`${word}, `)
                                    })}
                                </ul>
                            </div>
                        )
                    }) : <div/>}
                </div>

                <div>
                    <div id="lda-topic-bars" className="col-xs-12 empty_on_reset">

                    </div>
                    <div className="lda-topic-bar-template col-xs-12 template panel panel-default">
                        <strong><span className="lda-topic-bar-name col-xs-12" data-toggle="tooltip"
                                      data-placement="top" title=""></span></strong>
                    </div>
                </div>
            </div>
        )
    }

    // Das gleiche nochmals für den Vergleichsfall
    const SecondLDAResult = () => {
        return(
            <div className={"col-md-6"}>
                <div style={{minHeight: '350px'}}>
                    {state.secondLdaResult && state.secondLdaResult.topics ? Object.keys(state.secondLdaResult.topics).map((topic) => {
                        return (
                            <div>
                                {topic}:
                                <ul>
                                    {state.secondLdaResult.topics[topic].top_words.map((word) => {
                                        return (`${word}, `)
                                    })}
                                </ul>
                            </div>
                        )
                    }) : <div/>}
                </div>
                <div id="lda-second-topic-bars" className="col-xs-12 empty_on_reset">
                </div>
                <div className="lda-second-topic-bar-template col-xs-12 template panel panel-default">
                    <strong><span className="lda-second-topic-bar-name col-xs-12" data-toggle="tooltip"
                                  data-placement="top" title=""></span></strong>
                </div>
            </div>
        )
    }

    // Die Darstellung der gefundenen Emotions-Wörter bei der Wörterbuchanalyse, vereint Erstanalyse und Vergleichsfall
    const EmotionWordLists = () => {
        return(
            <div style={{marginBottom: '20px'}}>
                <div style={{marginLeft: '20px', marginRight: '20px', color: 'red'}}>
                    Warm:
                    <br/>
                    {state.emotionDictionaryResult && state.resultWarmWords.map((word) => {
                        return (
                            <span>{word}, </span>)
                    })}
                </div>
                <div style={{marginLeft: '20px', marginRight: '20px', color: 'blue'}}>
                    <br/>
                    Kalt:
                    <br/>
                    {state.emotionDictionaryResult && state.resultColdWords.map((word) => {
                        return (
                            <span>{word}, </span>)
                    })}
                </div>
            </div>
        )
    }

    // Die Darstellung der gefundenen Inhalts-Wörter bei der Wörterbuchanalyse, vereint Erstanalyse und Vergleichsfall
    const ContentWordLists = () => {
        return(
            <div style={{marginBottom: '20px'}}>
                <div style={{marginLeft: '20px', marginRight: '20px', color: 'red'}}>
                    Lebensort:
                    <br/>
                    {state.contentDictionaryResult && state.resultHomeWords.map((word) => {
                        return (
                            <span>{word}, </span>)
                    })}
                </div>
                <div style={{marginLeft: '20px', marginRight: '20px', color: 'blue'}}>
                    <br/>
                    Bildungsort:
                    <br/>
                    {state.contentDictionaryResult && state.resultSchoolWords.map((word) => {
                        return (
                            <span>{word}, </span>)
                    })}
                </div>
            </div>
        )
    }

    // Darstellung des Ergebnisses der Wörterbuchanalyse im gestackten Säulendiagramm.
    // Hier wurde sich für Recharts entschieden, aufgrund der möglichen Darstellungsweise von warmen und kalten
    // Ergebnissen in einer Säule mit unterschiedlichen Werten.
    const EmotionFirstBarChart = (props) => {
        return(
            <div className={props.className ? props.className : ''}>
                {Object.keys(state.emotionDictionaryBarData).length ?
                    <div className={"center"}>
                        <BarChart
                            width={600}
                            height={400}
                            data={state.emotionDictionaryBarData}
                            stackOffset="sign"
                            margin={{
                                top: 5, right: 30, left: 20, bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="name"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend/>
                            <ReferenceLine y={0} stroke="#000"/>
                            <Bar dataKey="Warm" fill="#F2314B" stackId="stack"/>
                            <Bar dataKey="Kalt" fill="#0F5B94" stackId="stack"/>
                        </BarChart>
                    </div>
                    : <div/>}
            </div>
        )
    }

    const ContentFirstBarChart = (props) => {
        return(
            <div className={props.className ? props.className : ''}>
                {Object.keys(state.contentDictionaryBarData).length ?
                    <div className={"row"}>
                        <BarChart
                            width={600}
                            height={400}
                            data={state.contentDictionaryBarData}
                            stackOffset="sign"
                            margin={{
                                top: 5, right: 30, left: 20, bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="name"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend/>
                            <ReferenceLine y={0} stroke="#000"/>
                            <Bar dataKey="Lebensort" fill="#F2314B" stackId="stack"/>
                        </BarChart>
                        <BarChart
                            width={600}
                            height={400}
                            data={state.contentDictionaryBarData}
                            stackOffset="sign"
                            margin={{
                                top: 5, right: 30, left: 20, bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="name"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend/>
                            <ReferenceLine y={0} stroke="#000"/>
                            <Bar dataKey="Bildungsort" fill="#0F5B94" stackId="stack"/>
                        </BarChart>
                    </div>
                    : <div/>}
            </div>
        )
    }

    // Das gleiche für den Vergleichsfall
    const EmotionSecondBarChart = () => {
        return(
            <div className={"col-md-6"}>
                {Object.keys(state.secondEmotionDictionaryBarData).length ?
                    <BarChart
                        width={600}
                        height={400}
                        data={state.secondEmotionDictionaryBarData}
                        stackOffset="sign"
                        margin={{
                            top: 5, right: 30, left: 20, bottom: 5,
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="name"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <ReferenceLine y={0} stroke="#000"/>
                        <Bar dataKey="Warm" fill="#F2314B" stackId="stack"/>
                        <Bar dataKey="Kalt" fill="#0F5B94" stackId="stack"/>
                    </BarChart>
                    : <div/>}
            </div>
        )
    }

    const ContentSecondBarChart = () => {
        return(
            <div className={"col-md-6"}>
                {Object.keys(state.secondContentDictionaryBarData).length ?
                    <div>
                        <BarChart
                            width={600}
                            height={400}
                            data={state.secondContentDictionaryBarData}
                            stackOffset="sign"
                            margin={{
                                top: 5, right: 30, left: 20, bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="name"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend/>
                            <ReferenceLine y={0} stroke="#000"/>
                            <Bar dataKey="Lebensort" fill="#F2314B" stackId="stack"/>
                        </BarChart>
                        <BarChart
                            width={600}
                            height={400}
                            data={state.secondContentDictionaryBarData}
                            stackOffset="sign"
                            margin={{
                                top: 5, right: 30, left: 20, bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="name"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend/>
                            <ReferenceLine y={0} stroke="#000"/>
                            <Bar dataKey="Bildungsort" fill="#0F5B94" stackId="stack"/>
                        </BarChart>
                    </div>
                    : <div/>}
            </div>
        )
    }

    // Mithilfe von Tabs kann zwischen den Ergebnissen der LDA- und Wörterbuchanalyse hin- und hergewechselt werden
    return (
        <Tabs onChange={(value) => {
            setState({selectedTab: value})
        }}>
            <Tab label={"LDA"} value={"lda"} onActive={() => {
                setState({selectedTab: 'lda'}, () => {
                    // Zeichne LDA nochmals, da bei Tabwechsel sonst nicht nochmal gerendert wird
                    paint_topicbars(false, state.topicbarData, state.ldaResult.topics)
                    if(state.second){
                        paint_topicbars(true, state.topicbarData, state.ldaResult.topics)
                    }
                })
            }}>
                {!state.second ?
                    <div>
                        <FirstLDAResult className={"col-md-12"}/>
                    </div>
                    :
                    <div className={"row"}>
                        <FirstLDAResult className={"col-md-6"} style={{minHeight: '350px'}}/>
                        <hr/>
                        <SecondLDAResult/>
                        <hr/>
                    </div>
                }
            </Tab>
            <Tab label={"Inhalts-Wörterbuch"} value={"contentDictionary"} onActive={() => {
                setState({selectedTab: 'contentDictionary'})
            }}>
                {state.second ?
                    <div className={"row"}>
                        <ContentWordLists/>
                        <ContentFirstBarChart className={"col-md-6"}/>
                        <ContentSecondBarChart/>
                    </div>

                    :
                    <div>
                        <ContentWordLists/>
                        <ContentFirstBarChart/>
                    </div>}

                <hr/>
            </Tab>
            <Tab label={"Emotions-Wörterbuch"} value={"emotionDictionary"} onActive={() => {
                setState({selectedTab: 'emotionDictionary'})
            }}>
                {state.second ?
                    <div className={"row"}>
                        <EmotionWordLists/>
                        <EmotionFirstBarChart className={"col-md-6"}/>
                        <EmotionSecondBarChart/>
                    </div>

                    :
                    <div>
                        <EmotionWordLists/>
                        <EmotionFirstBarChart/>
                    </div>}

                <hr/>
            </Tab>
        </Tabs>
    )
}

export default Results;
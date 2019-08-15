import React from 'react'
import {Tabs, Tab} from 'material-ui/Tabs'
import {
    BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine,
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

    // Die Darstellung der gefundenen Wörter bei der Wörterbuchanalyse, vereint Erstanalyse und Vergleichsfall
    const WordLists = () => {
        return(
            <div style={{marginBottom: '20px'}}>
                <div style={{marginLeft: '20px', marginRight: '20px', color: 'red'}}>
                    Warm:
                    <br/>
                    {state.dictionaryResult && state.resultWarmWords.map((word) => {
                        return (
                            <span>{word}, </span>)
                    })}
                </div>
                <div style={{marginLeft: '20px', marginRight: '20px', color: 'blue'}}>
                    <br/>
                    Kalt:
                    <br/>
                    {state.dictionaryResult && state.resultColdWords.map((word) => {
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
    const FirstBarChart = (props) => {
        return(
            <div className={props.className ? props.className : ''}>
                {Object.keys(state.dictionaryBarData).length ?
                    <div className={"center"}>
                        <BarChart
                            width={600}
                            height={400}
                            data={state.dictionaryBarData}
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

    // Das gleiche für den Vergleichsfall
    const SecondBarChart = () => {
        return(
            <div className={"col-md-6"}>
                {Object.keys(state.secondDictionaryBarData).length ?
                    <BarChart
                        width={600}
                        height={400}
                        data={state.secondDictionaryBarData}
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

    // Mithilfe von Tabs kann zwischen den Ergebnissen der LDA- und Wörterbuchanalyse hin- und hergewechselt werden
    return (
        <Tabs onChange={(value) => {
            setState({selectedTab: value})
        }}>
            <Tab label={"LDA"} value={"lda"} onActive={() => {
                setState({selectedTab: 'lda'})
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
            <Tab label={"Wörterbuch"} value={"dictionary"} onActive={() => {
                setState({selectedTab: 'dictionary'})
            }}>
                {state.second ?
                    <div className={"row"}>
                        <WordLists/>
                        <FirstBarChart className={"col-md-6"}/>
                        <SecondBarChart/>
                    </div>

                    :
                    <div>
                        <WordLists/>
                        <FirstBarChart/>
                    </div>}

                <hr/>
            </Tab>
        </Tabs>
    )
}

export default Results;
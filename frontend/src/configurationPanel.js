import React from 'react'
import SelectField from 'material-ui/SelectField'
import TextField from 'material-ui/TextField'
import MenuItem from 'material-ui/MenuItem'
import RaisedButton from 'material-ui/RaisedButton'
import DatePicker from 'material-ui/DatePicker'
import 'bootstrap/dist/css/bootstrap.css';
import getCookie from './Helper/getCookie'
import {buildDictionaryBarData, buildTopicBarData} from './Helper/charts'
import axios from "axios";
import moment from 'moment'
import 'bootstrap/dist/css/bootstrap.css';

const ConfigurationPanel = (props) => {
    const {state, setState} = props

    /* Diese Funktion startet die Analyse mithilfe eines Calls an den Server. Dafür wird ein POST-Request mit der
       Config, dem ausgewählten Fall und den Start- und Enddaten genutzt. Zusätzlich muss ein CSRF-Token im Header
       gesetzt werden, damit der Server den Request akzeptiert.
     */
    const startAnalysis = () => {
        setState({loading: true})
        let config = {
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
            }
        }
        axios.post('start-analysis/', {
            chosenCaseId: state.chosenCaseId,
            start: state.start,
            end: state.end,
            config: state.config
        }, config)
            .then(
            res => {
                // Wenn Status des Requests 200 ==> Call war erfolgreich, Ergebnisdaten in den State übernehmen
                if(res.status === 200){
                    setState({
                    comments: res.data['hours'],
                    ldaResult: res.data['lda_result'],
                    dictionaryResult: res.data['dictionary_result'],
                    resultWarmWords: res.data['warm_words'],
                    resultColdWords: res.data['cold_words'],
                    loading: false
                }, () => {
                        // anschließend die Daten für die Charts vorbereiten
                    buildTopicBarData(res.data['lda_result']['entries'],
                        res.data['lda_result']['topics'], false, setState, state)
                    buildDictionaryBarData(res.data['dictionary_result'], false, setState)
                })
                }else{
                    // Bei Status 204 lagen keine Texte vor und es konnte nichts analysiert werden.
                    if(res.status === 204){
                        alert('Keine Texte gefunden.')
                        setState({loading: false})
                    }
                }
            })
            .catch(err => {setState({loading: false}); alert(err)});
    }

    /* Ähnlich wie die erste Funktion, nur wird hier der Vergleichsfall analysiert */
    const startSecondAnalysis = () => {
        setState({loading: true})
        let config = {
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
            }
        }
        axios.post('start-analysis/', {
            chosenCaseId: state.secondCaseId,
            start: state.start,
            end: state.end,
            config: state.config
        }, config)
            .then(res => setState({
                comments: state.comments.concat(res.data['hours']),
                second: true,
                resultWarmWords: state.resultWarmWords.concat(res.data['warm_words']),
                resultColdWords: state.resultColdWords.concat(res.data['cold_words']),
                secondLdaResult: res.data['lda_result'],
                secondDictionaryResult: res.data['dictionary_result'],
                loading: false
            }, () => {
                buildTopicBarData(res.data['lda_result']['entries'], res.data['lda_result']['topics'], true, setState, state)
                buildDictionaryBarData(res.data['dictionary_result'], true, setState)
            }))
            .catch(err => {setState({loading: false}); alert(err)});
    }

    // Helper-Funktion zum Setzen der verschiedenen Felder in der Config für die Analyse
    const setConfig = (fieldName, value) => {
        let config = state.config
        config[fieldName] = value
        setState({config: config})
    }
    return(
        <div className="row">
            <div className="col-md-3">
                <SelectField
                    floatingLabelText={"Fall-ID"}
                    onChange={(e, index, value) => {
                        setState({chosenCaseId: value})
                    }}
                    value={state.chosenCaseId}
                    style={{float: 'left', marginLeft: '20px', marginRight: '20px'}}
                >
                    {state.caseIdOptions.map((caseId) => {
                        return (<MenuItem primaryText={caseId} value={caseId}/>)
                    })}
                </SelectField>
                <SelectField
                    floatingLabelText={"Vergleichsfall"}
                    onChange={(e, index, value) => {
                        setState({secondCaseId: value})
                    }}
                    value={state.secondCaseId}
                    style={{float: 'left', marginLeft: '20px', marginRight: '20px'}}
                >
                    {state.caseIdOptions.map((caseId) => {
                        return (<MenuItem primaryText={caseId} value={caseId}/>)
                    })}
                </SelectField>
                <DatePicker
                    hintText={"Startdatum"}
                    defaultDate={new Date(2018, 0, 1)}
                    onChange={(e, newValue) => {
                        setState({start: moment(newValue).format("YYYY-MM-DD")})
                    }}
                />
                <DatePicker
                    hintText={"Enddatum"}
                    defaultDate={new Date(2019, 0, 1)}
                    onChange={(e, newValue) => {
                        setState({end: moment(newValue).format("YYYY-MM-DD")})
                    }}
                />
                <TextField floatingLabelText={"Anzahl der zusammenzufassenden Tage"} onChange={(e, newValue) => {
                    setConfig('timespan', newValue)
                }} value={state.config.timespan}/>

                <RaisedButton style={{marginTop: '20px', width: '100%'}} disabled={state.loading}
                              label={state.loading ? 'Warte auf Antwort...' : "Analyse starten"}
                              onClick={() => {
                                  startAnalysis()
                              }}/>
                <RaisedButton style={{marginTop: '20px', width: '100%'}} disabled={state.loading}
                              label={state.loading ? 'Warte auf Antwort...' : "Vergleichsfall analysieren"}
                              onClick={() => {
                                  startSecondAnalysis()
                              }}/>
            </div>
            <div className="col-md-3">
                <TextField floatingLabelText={"Anzahl der Themen"} onChange={(e, newValue) => {
                    setConfig('numberOfTopics', newValue)
                }} value={state.config.numberOfTopics}/>
                <TextField floatingLabelText={"Dirichlet Alpha"} onChange={(e, newValue) => {
                    setConfig('dirichletAlpha', newValue)
                }} value={state.config.dirichletAlpha}/>
                <TextField floatingLabelText={"Dirichlet Eta"} onChange={(e, newValue) => {
                    setConfig('dirichletEta', newValue)
                }} value={state.config.dirichletEta}/>
                <TextField floatingLabelText={"Anzahl der Iterationen"} onChange={(e, newValue) => {
                    setConfig('numberOfIterations', newValue)
                }} value={state.config.numberOfIterations}/>
                <SelectField floatingLabelText={"Wörterbuch"} onChange={(e, index, newValue) => {
                    setConfig('dictionary', newValue)
                }} value={state.config.dictionary}>
                    <MenuItem primaryText={"Einfach"} value={'simple'}/>
                    <MenuItem primaryText={"Angereichert"} value={'enriched'}/>
                </SelectField>
            </div>
            <div className="col-md-3">
                <TextField floatingLabelText={"Anzahl der dargestellten Top-Themen"}
                           onChange={(e, newValue) => {
                               setConfig('numberOfDisplayedTopTopics', newValue)
                           }} value={state.config.numberOfDisplayedTopTopics}/>
                <TextField floatingLabelText={"Anzahl der dargestellten Top-Wörter"}
                           onChange={(e, newValue) => {
                               setConfig('displayedTopicsTopWords', newValue)
                           }} value={state.config.displayedTopicsTopWords}/>
                <SelectField floatingLabelText={"Stammwortreduktion"} onChange={(e, index, newValue) => {
                    setConfig('stemming', newValue)
                }} value={state.config.stemming}>
                    <MenuItem primaryText={"Ja"} value={true}/>
                    <MenuItem primaryText={"Nein"} value={false}/>
                </SelectField>
                <SelectField floatingLabelText={"Stoppwortreduktion"} onChange={(e, index, newValue) => {
                    setConfig('removeStopwords', newValue)
                }} value={state.config.removeStopwords}>
                    <MenuItem primaryText={"Ja"} value={true}/>
                    <MenuItem primaryText={"Nein"} value={false}/>
                </SelectField>
            </div>
            <div className="col-md-3">
                <TextField floatingLabelText={"Frequenz der zu entfernenden hoch-frequenten Wörter"}
                           onChange={(e, newValue) => {
                               setConfig('removeHighFrequentWords', newValue)
                           }} value={state.config.removeHighFrequentWords}/>
                <SelectField floatingLabelText={"Groß-Kleinschreibung ignorieren"}
                             onChange={(e, index, newValue) => {
                                 setConfig('ignoreCapitalization', newValue)
                             }} value={state.config.ignoreCapitalization}>
                    <MenuItem primaryText={"Ja"} value={true}/>
                    <MenuItem primaryText={"Nein"} value={false}/>
                </SelectField>
                <SelectField floatingLabelText={"Zahlen entfernen"} onChange={(e, index, newValue) => {
                    setConfig('removeNumbers', newValue)
                }} value={state.config.removeNumbers}>
                    <MenuItem primaryText={"Ja"} value={true}/>
                    <MenuItem primaryText={"Nein"} value={false}/>
                </SelectField>
                <TextField floatingLabelText={"Minimale Wortlänge"} onChange={(e, newValue) => {
                    setConfig('minimalWordLength', newValue)
                }} value={state.config.minimalWordLength}/>
            </div>
        </div>
    )
}

export default ConfigurationPanel;
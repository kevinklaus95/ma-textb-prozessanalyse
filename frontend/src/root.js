import React from 'react'
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.css';
import CustomAnalysis from './customAnalysis'
import ConfigurationPanel from './configurationPanel'
import Results from './results'
import DataTable from './dataTable'

/* Diese React Komponente stellt die Wurzel der Anwendung dar und beinhaltet alle anderen Teilkomponenten.
    Im State werden die frontendseitig notwendigen Daten gemanaget.
 */
class Root extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            caseIdOptions: [],
            chosenCaseId: null,
            secondCaseId: null,
            start: "2018-01-01",
            end: "2019-01-01",
            config: {
                numberOfTopics: 3,
                dirichletAlpha: 0.00001,
                dirichletEta: 0.00001,
                numberOfIterations: 6000,
                randomSeed: 1,
                numberOfDisplayedTopTopics: 3,
                displayedTopicsTopWords: 8,
                removeHighFrequentWords: 2,
                ignoreCapitalization: false,
                removeNumbers: true,
                stemming: false,
                removeStopwords: true,
                minimalWordLength: 3,
                timespan: 14,
                emotionDictionary: 'enriched',
                contentDictionary: 'enriched',
                selectedTab: 'lda'
            },
            comments: [],
            ldaResult: null,
            secondldaResult: null,
            emotionDictionaryResult: null,
            secondEmotionDictionaryResult: null,
            contentDictionaryResult: null,
            secondContentDictionaryResult: null,
            loading: false,
            topicbarData: {},
            secondTopicbarData: {},
            emotionDictionaryBarData: {},
            secondEmotionDictionaryBarData: {},
            contentDictionaryBarData: {},
            secondContentDictionaryBarData: {},
            second: false,
            customText: '',
            resultColdWords: [],
            resultWarmWords: [],
            resultSchoolWords: [],
            resultHomeWords: []
        };
    }

    /*
    componentDidMount() wird direkt gecallt wenn die App aufgerufen wird. Hier geht ein Call an den Server, um die
    verschiedenen Fall IDs aus der Datenbank zu erfragen. Anschließend werden 2 relevante IDs direkt als Standard
    gesetzt.
     */

    componentDidMount(){
        axios.get('api/distinct-project-ids/')
            .then(res => this.setState({caseIdOptions: res.data.project_ids}, () => {
                this.setState({chosenCaseId: 142, secondCaseId: 405})
            }))
            .catch(err => console.log(err));
    }

    /* In der Render-Methode werden alle notwendigen Teilkomponenten aufgerufen und der State sowie die Methode
       zum Manipulieren des States weitergegeben.
     */
    render() {
        return (
            <div>
                <CustomAnalysis state={this.state} setState={(args, successCallback) => {
                    this.setState(args, successCallback)
                }}/>
                <ConfigurationPanel state={this.state} setState={(args, successCallback) => {
                    this.setState(args, successCallback)
                }}/>
                <hr/>
                <Results state={this.state} setState={(args, successCallback) => {
                    this.setState(args, successCallback)
                }}/>
                <DataTable state={this.state} setState={(args, successCallback) => {
                    this.setState(args, successCallback)
                }}/>
                <hr/>
            </div>
        );

    }
}

export default Root
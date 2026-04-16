import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import KeywordInput from './pages/KeywordInput';
import AnalysisDashboard from './pages/AnalysisDashboard';
import ContentEditorPage from './pages/ContentEditorPage';
import GraphVisualization from './pages/GraphVisualization';
import RankingPrediction from './pages/RankingPrediction';
import RecommendationPanel from './pages/RecommendationPanel';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<KeywordInput />} />
          <Route path="analyze" element={<AnalysisDashboard />} />
          <Route path="editor" element={<ContentEditorPage />} />
          <Route path="graph" element={<GraphVisualization />} />
          <Route path="predict" element={<RankingPrediction />} />
          <Route path="recommend" element={<RecommendationPanel />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

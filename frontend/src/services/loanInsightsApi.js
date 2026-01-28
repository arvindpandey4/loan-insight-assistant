const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const fetchDashboardStats = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard-stats`);
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Failed to fetch dashboard stats:", error);
    throw error;
  }
};

export const queryLoanInsights = async (question, conversationHistory = null) => {
  try {
    const requestBody = { query: question };

    // Add conversation history if provided
    if (conversationHistory && conversationHistory.length > 0) {
      requestBody.conversation_history = conversationHistory;
    }

    const response = await fetch(`${API_BASE_URL}/query-loan-insights`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    const data = await response.json();

    // Transform backend response to frontend format if needed
    // Backend returns: { answer, risk_notes, evidence_points, source, ... }
    return {
      similar_cases_found: data.structured_data ? data.structured_data.length : 0,
      common_risk_factors: data.risk_notes || [],
      historical_trend: "Based on analysis of similar historical cases",
      explanation: data.answer,
      confidence: 0.85,
      source: data.source || 'rag',
      // Pass full data for advanced use
      ...data
    };
  } catch (error) {
    console.error("Failed to query loan insights:", error);
    throw error;
  }
};

export const fetchLoanStatusDistribution = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/analytics/loan-status`);
    if (!response.ok) throw new Error("Failed to fetch loan status data");
    return await response.json();
  } catch (error) {
    console.error("Analytics API Error:", error);
    throw error;
  }
};

export const fetchAvgCIBIL = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/analytics/cibil-by-status`);
    if (!response.ok) throw new Error("Failed to fetch CIBIL data");
    return await response.json();
  } catch (error) {
    console.error("Analytics API Error:", error);
    throw error;
  }
};

export const fetchRejectionReasons = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/analytics/rejections-by-purpose`);
    if (!response.ok) throw new Error("Failed to fetch rejection data");
    return await response.json();
  } catch (error) {
    console.error("Analytics API Error:", error);
    throw error;
  }
};
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

export const queryLoanInsights = async (question) => {
  try {
    const response = await fetch(`${API_BASE_URL}/query-loan-insights`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: question }),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    const data = await response.json();

    // Transform backend response to frontend format if needed
    // Backend returns: { answer, risk_notes, evidence_points, ... }
    return {
      similar_cases_found: data.structured_data ? data.structured_data.length : 0,
      common_risk_factors: data.risk_notes || [],
      historical_trend: "Based on analysis of similar historical cases", // Backend doesn't give a summary string yet
      explanation: data.answer,
      confidence: 0.85, // Backend might not calculate confidence score yet
      // Pass full data for advanced use
      ...data
    };
  } catch (error) {
    console.error("Failed to query loan insights:", error);
    throw error;
  }
};
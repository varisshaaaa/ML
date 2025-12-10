import { useState, useEffect } from 'react'
import { Activity, Wind, AlertTriangle, MapPin, BarChart3, Droplets, Thermometer } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface AQIData {
    city: string
    aqi: number
    pm2_5: number
    pm10: number
    no2: number
    so2: number
    o3: number
    co: number
    timestamp: string
}

interface PredictionResult {
    predicted_aqi: number
    risk_level: string
    health_risk_score: number
}

function App() {
    const [selectedCity, setSelectedCity] = useState<string>('Lahore')
    const [currentData, setCurrentData] = useState<AQIData | null>(null)
    const [prediction, setPrediction] = useState<PredictionResult | null>(null)
    const [loading, setLoading] = useState(false)

    // Mock historical data for the chart
    health_risk_score: 75
})
            }
        } catch (error) {
    console.error("Prediction failed", error)
}
    }

useEffect(() => {
    fetchCityData(selectedCity)
}, [selectedCity])

const getAQIColor = (aqi: number) => {
    if (aqi <= 50) return 'text-green-400'
    if (aqi <= 100) return 'text-yellow-400'
    if (aqi <= 150) return 'text-orange-400'
    if (aqi <= 200) return 'text-red-400'
    return 'text-purple-400'
}

return (
    <div className="min-h-screen bg-background text-white p-6 md:p-12">
        <div className="max-w-7xl mx-auto space-y-8">

            {/* Header */}
            <header className="flex flex-col md:flex-row justify-between items-center gap-4 border-b border-surface pb-6">
                <div className="flex items-center gap-3">
                    <div className="p-3 bg-primary/20 rounded-xl">
                        <Activity className="w-8 h-8 text-primary" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
                            AirHealth AI
                        </h1>
                        <p className="text-gray-400 text-sm">Real-time Advanced Monitoring System</p>
                    </div>
                </div>

                <div className="flex items-center gap-4 bg-surface p-2 rounded-lg">
                    <MapPin className="text-gray-400 w-5 h-5" />
                    <select
                        value={selectedCity}
                        onChange={(e) => setSelectedCity(e.target.value)}
                        className="bg-transparent border-none outline-none text-white font-medium cursor-pointer"
                    >
                        {['Lahore', 'Karachi', 'Islamabad', 'Faisalabad', 'Multan'].map(city => (
                            <option key={city} value={city} className="bg-surface">{city}</option>
                        ))}
                    </select>
                </div>
            </header>

            {/* Main Dashboard Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Left Column: Current Status */}
                <div className="lg:col-span-2 space-y-6">

                    {/* AQI Card */}
                    <div className="bg-surface rounded-2xl p-6 border border-white/5 relative overflow-hidden group hover:border-primary/30 transition-all">
                        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <Wind className="w-32 h-32" />
                        </div>

                        <div className="relative z-10">
                            <div className="flex justify-between items-start mb-8">
                                <div>
                                    <h2 className="text-lg text-gray-400 font-medium">Current Air Quality</h2>
                                    <p className="text-xs text-gray-500">Updated: {new Date().toLocaleTimeString()}</p>
                                </div>
                                <span className={`px-4 py-1 rounded-full text-xs font-bold bg-white/5 border border-white/10 ${currentData ? getAQIColor(currentData.aqi) : ''}`}>
                                    {currentData?.aqi ? (currentData.aqi > 150 ? 'Unhealthy' : 'Moderate') : 'Loading...'}
                                </span>
                            </div>

                            <div className="flex items-end gap-4">
                                <span className={`text-7xl font-bold ${currentData ? getAQIColor(currentData.aqi) : 'text-gray-600'}`}>
                                    {currentData ? currentData.aqi : '--'}
                                </span>
                                <div className="mb-4 text-gray-400">
                                    <p className="text-sm font-medium">US AQI</p>
                                    <p className="text-xs">PM2.5: {currentData?.pm2_5.toFixed(1)} µg/m³</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Pollutants Grid */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {[
                            { label: 'PM10', value: currentData?.pm10, unit: 'µg/m³', icon: Wind },
                            { label: 'NO2', value: currentData?.no2, unit: 'ppb', icon: Droplets },
                            { label: 'SO2', value: currentData?.so2, unit: 'ppb', icon: Thermometer },
                            { label: 'O3', value: currentData?.o3, unit: 'ppb', icon: Activity },
                        ].map((item, i) => (
                            <div key={i} className="bg-surface p-4 rounded-xl border border-white/5 hover:bg-white/5 transition-colors">
                                <div className="flex items-center gap-2 mb-2 text-gray-400">
                                    <item.icon className="w-4 h-4" />
                                    <span className="text-xs font-medium">{item.label}</span>
                                </div>
                                <p className="text-xl font-semibold">{item.value?.toFixed(1) || '--'}</p>
                                <p className="text-[10px] text-gray-500">{item.unit}</p>
                            </div>
                        ))}
                    </div>

                    {/* Chart */}
                    <div className="bg-surface rounded-2xl p-6 border border-white/5">
                        <h3 className="text-lg font-medium mb-6 flex items-center gap-2">
                            <BarChart3 className="w-5 h-5 text-primary" />
                            24h Trend
                        </h3>
                        <div className="h-64 data-[loading=true]:opacity-50" data-loading={loading}>
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={historyData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                    <XAxis dataKey="time" stroke="#666" tick={{ fontSize: 12 }} />
                                    <YAxis stroke="#666" tick={{ fontSize: 12 }} />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#18181b', border: '1px solid #333', borderRadius: '8px' }}
                                        itemStyle={{ color: '#fff' }}
                                    />
                                    <Line type="monotone" dataKey="aqi" stroke="#3b82f6" strokeWidth={3} dot={{ fill: '#3b82f6', r: 4 }} activeDot={{ r: 6 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                </div>

                {/* Right Column: AI Prediction */}
                <div className="lg:col-span-1">
                    <div className="bg-gradient-to-b from-surface to-background rounded-2xl p-6 border border-white/5 h-full flex flex-col">
                        <div className="mb-6">
                            <h2 className="text-xl font-bold flex items-center gap-2">
                                <Activity className="text-secondary w-6 h-6" />
                                Health Forecast
                            </h2>
                            <p className="text-sm text-gray-400 mt-2">AI-powered risk assessment for the next hour.</p>
                        </div>

                        {!prediction ? (
                            <div className="flex-1 flex flex-col items-center justify-center p-8 border-2 border-dashed border-white/10 rounded-xl">
                                <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-4">
                                    <Activity className="w-8 h-8 text-gray-500" />
                                </div>
                                <button
                                    onClick={handlePredict}
                                    className="px-6 py-3 bg-primary hover:bg-blue-600 active:scale-95 transition-all rounded-lg font-semibold shadow-lg shadow-blue-500/20"
                                >
                                    Run Prediction
                                </button>
                            </div>
                        ) : (
                            <div className="flex-1 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                                <div className={`p-6 rounded-xl border ${prediction.risk_level === 'High' ? 'bg-red-500/10 border-red-500/50' :
                                    prediction.risk_level === 'Moderate' ? 'bg-orange-500/10 border-orange-500/50' : 'bg-green-500/10 border-green-500/50'
                                    }`}>
                                    <div className="flex items-center gap-3 mb-2">
                                        <AlertTriangle className={`w-5 h-5 ${prediction.risk_level === 'High' ? 'text-red-500' :
                                            prediction.risk_level === 'Moderate' ? 'text-orange-500' : 'text-green-500'
                                            }`} />
                                        <span className="font-bold uppercase tracking-wider text-sm">Risk Level</span>
                                    </div>
                                    <p className={`text-3xl font-bold ${prediction.risk_level === 'High' ? 'text-red-400' :
                                        prediction.risk_level === 'Moderate' ? 'text-orange-400' : 'text-green-400'
                                        }`}>
                                        {prediction.risk_level}
                                    </p>
                                </div>

                                <div className="space-y-4">
                                    <div className="flex justify-between items-center p-4 bg-white/5 rounded-lg">
                                        <span className="text-gray-400">Predicted AQI</span>
                                        <span className="text-xl font-mono">{prediction.predicted_aqi.toFixed(0)}</span>
                                    </div>
                                    <div className="flex justify-between items-center p-4 bg-white/5 rounded-lg">
                                        <span className="text-gray-400">Health Score</span>
                                        <div className="flex items-center gap-2">
                                            <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-gradient-to-r from-green-500 to-red-500"
                                                    style={{ width: `${prediction.health_risk_score}%` }}
                                                />
                                            </div>
                                            <span className="text-sm font-mono">{prediction.health_risk_score.toFixed(0)}</span>
                                        </div>
                                    </div>
                                </div>

                                <button
                                    onClick={() => setPrediction(null)}
                                    className="w-full py-3 border border-white/10 hover:bg-white/5 rounded-lg text-sm transition-colors"
                                >
                                    Clear Prediction
                                </button>
                            </div>
                        )}
                    </div>
                </div>

            </div>
        </div>
    </div>
)
}

export default App

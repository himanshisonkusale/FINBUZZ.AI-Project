import React from 'react';
import { 
  Target, 
  TrendingUp, 
  Shield, 
  Zap, 
  BarChart3, 
  PieChart, 
  AlertTriangle, 
  Smartphone,
  MessageCircle,
  Users
} from 'lucide-react';
import { motion } from 'framer-motion';

const Features = () => {
  const personalizedTools = [
    {
      icon: Smartphone,
      title: "Voice Interaction, JSON Data Input & Report Generator",
      description: "Speak queries, upload financial data in JSON, and get PDF financial health reports."
    },
    {
      icon: TrendingUp,
      title: "Net Worth & Projection Tracker, Financial Health Score",
      description: "Track net worth, project future milestones, and get a 0–100 health score."
    },
    {
      icon: PieChart,
      title: "SIP & Mutual Fund Analyzer, Diversification Checker",
      description: "Identify weak SIPs, benchmark funds, and detect overexposure to sectors/assets."
    },
    {
      icon: AlertTriangle,
      title: "Loan Affordability & Debt Optimization Advisor",
      description: "Simulate loan EMI & burden, and prioritize debts to minimize interest."
    },
    {
      icon: Shield,
      title: "Green Investing & Behavioral Bias Alerts",
      description: "Highlight ESG investments and flag risky behaviors like panic-selling or overtrading."
    },
    
  ];

  const analyticsTools = [
    {
      icon: BarChart3,
      title: "Forecaster, Macro-Economic Dashboard, Sector Picker",
      description: "Projects future performance, analyzes macro trends & indices, and suggests promising sectors."
    },
    {
      icon: TrendingUp,
      title: "Smart Stock Screener, Sentiment Engine, Valuation Comparator",
      description: "Finds strong stocks, rates sentiment from news/social, and checks valuations vs peers/history."
    },
    {
      icon: PieChart,
      title: "Portfolio Builder, Rebalancer, Risk Heatmap",
      description: "Builds & optimizes portfolios, suggests rebalancing, and visualizes portfolio risk exposure."
    },
    {
      icon: Smartphone,
      title: "IPO Advisor, Event-Driven Detector, Dividend Optimizer",
      description: "Evaluates IPOs, flags special situations (mergers, buybacks), and recommends high yield stocks."
    },
    {
      icon: Target,
      title: "Thematic Portfolio Creator, Sector Rotation Advisor, Custom NLP Screening",
      description: "Creates theme-based portfolios, suggests sector shifts, and screens stocks using natural language commands."
    },
    
  ];

  const bankingQueries = [
    {
      icon: MessageCircle,
      title: "Intelligent AI Agent with Chat/Voice First Functionality",
      description: "This agent operates with various modes, including customer queries, crisis mode, fraud detection mode, and financial therapy mode."
    },
    {
      icon: Zap,
      title: "Intelligent Query Processing",
      description: "Advanced AI understanding of complex banking and financial queries with contextual responses, and automating workflows such as scheduling calls or appointments."
    },
    {
      icon: Users,
      title: "24/7 Customer Support",
      description: "Round-the-clock automated customer service with seamless escalation to human experts."
    }
  ];

  const tradingInvestingTools = [
    {
        icon: Zap,
        title: "Real-time Trading Data",
        description: "Fetches real-time intra day trading data through the yfinance API."
    },
    {
        icon: BarChart3,
        title: "Pre/Post Trading Day Analysis",
        description: "Provides pre-trading day and post-trading day analysis through candlestick charts."
    },
    {
        icon: Shield,
        title: "Multi-Agentic Framework",
        description: "Utilizes a multi-agentic framework trained with robust financial strategies and advanced analytics to reduce risk and increase profit."
    },
    {
        icon: PieChart,
        title: "Analytics Dashboard",
        description: "Offers an analytics dashboard with real-time analysis and logs of trades (buy, sold, or hold), a profit and loss chart, win rate, and more."
    }
  ];

  const FeatureCard = ({ icon: Icon, title, description, index }: { icon: any, title: string, description: string, index: number }) => (
    <motion.div 
      className="group bg-charcoal-900/80 backdrop-blur-sm p-6 rounded-xl border border-electric-blue-500/30 hover:border-electric-blue-500/60 transition-all duration-100 hover:transform hover:scale-105 hover:rotate-1 shadow-glow-md hover:shadow-electric-blue animate-fadeInUp opacity-0"
      style={{ 
        animationDelay: `${index * 0.1}s`,
        animationFillMode: 'forwards'
      }}
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.05, transition: { duration: 0.1 } }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.6 }}
    >
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <div className="w-12 h-12 bg-gradient-to-r from-electric-blue-500/30 to-deep-purple-600/30 rounded-lg flex items-center justify-center group-hover:from-electric-blue-500/50 group-hover:to-deep-purple-600/50 transition-all duration-100 group-hover:scale-125 group-hover:rotate-12 shadow-electric-blue group-hover:shadow-deep-purple">
            <Icon className="w-6 h-6 text-[#e45619] group-hover:text-[#dd6c1c] transition-colors duration-300" />
          </div>
        </div>
        <div>
          <h3 className="text-lg font-semibold text-text-primary mb-2 group-hover:text-electric-blue-300 transition-colors duration-300">{title}</h3>
          <p className="text-text-muted leading-relaxed group-hover:text-text-secondary transition-colors duration-300">{description}</p>
        </div>
      </div>
    </motion.div>
  );

  return (
    <motion.section 
      id="features" 
      className="py-20 bg-deep-black relative overflow-hidden"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.8, delay: 0.2 }}
    >
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        
        <motion.div 
          className="text-center mb-16 transform hover:scale-105 transition-transform duration-700"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.2 }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-5xl sm:text-4xl lg:text-5xl font-bold mb-4">
  <span className="text-white">Powerful Features of </span>
  <span className="text-[#00FF88] drop-shadow-[0_0_7px_#00FF88]">FINBUZZ.AI</span>
</h2>
<p className="text-xl text-transparent bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text max-w-3xl mx-auto">
          Revolutionizing financial services with cutting-edge AI technology and comprehensive analytical tools.
          </p>
        </motion.div>

        {/* Personalised Banking Queries and Customer Queries */}
        <div className="mb-16">
          <motion.h3 
            className="text-3xl font-bold mb-8 text-center"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6 }}
          >
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#e45619] to-[#dd6c1c]">Personalised Banking Queries & Customer Queries</span>
          </motion.h3>


          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
  {bankingQueries.map((feature, index) => (
    <motion.div 
      key={index} 
      className="relative group overflow-hidden bg-gradient-to-br from-space-blue-900/40 via-space-blue-950/60 to-deep-black/80 backdrop-blur-md p-6 rounded-xl border border-gray-700 h-auto min-h-48 w-auto max-w-sm mx-auto transition-transform duration-100 hover:scale-105"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      whileHover={{ scale: 1.05, transition: { duration: 0.1 } }}
    >
      <div className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_center,rgba(109,40,217,0.5)_0%,transparent_70%)] opacity-0 transition-opacity duration-500 group-hover:opacity-100"></div>
      <div className="relative z-10 flex flex-col items-center text-center h-full">
        <div className="w-12 h-12 bg-gradient-to-r from-electric-blue-500/30 to-deep-purple-600/30 rounded-lg flex items-center justify-center mb-4">
          <feature.icon className="w-6 h-6 text-[#e45619] group-hover:text-[#dd6c1c] transition-colors duration-300" />
        </div>
        <h4 className="text-xl font-semibold text-text-primary mb-2">{feature.title}</h4>
        <p className="text-text-muted text-base leading-relaxed">{feature.description}</p>
      </div>
    </motion.div>
  ))}
</div>

        </div>

        {/* Personalised Financial Tools */}
        <div className="mb-16">
          <motion.h3 
            className="text-3xl font-bold mb-8 text-center"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6 }}
          >
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#e45619] to-[#dd6c1c]">Personalised Financial Tools</span>
          </motion.h3>
          <div className="grid grid-cols-1 gap-4 mb-16">
  {personalizedTools.map((feature, index) => (
    <motion.div 
      key={index} 
      className="relative group overflow-hidden bg-gradient-to-br from-space-blue-900/40 via-space-blue-950/60 to-deep-black/80 backdrop-blur-md p-4 rounded-xl border border-gray-700 h-auto min-h-24 transition-transform duration-100 hover:scale-105 hover:border-electric-blue-400"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      whileHover={{ scale: 1.05, transition: { duration: 0.1 } }}
    >
      <div className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_center,rgba(109,40,217,0.5)_0%,transparent_70%)] opacity-0 transition-opacity duration-500 group-hover:opacity-100"></div>
      <div className="relative z-10 flex items-start space-x-3 h-full">
        <div className="w-8 h-8 bg-gradient-to-r from-electric-blue-500/30 to-deep-purple-600/30 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
          <feature.icon className="w-4 h-4 text-[#e45619] rounded-full animate-pulse group-hover:text-[#dd6c1c] transition-colors duration-300" />
        </div>
        <div className="flex-1">
          <h4 className="text-base font-semibold text-text-primary mb-2 leading-tight">{feature.title}</h4>
          <p className="text-text-muted text-sm leading-relaxed">{feature.description}</p>
        </div>
      </div>
    </motion.div>
  ))}
</div>


        </div>

        {/* Financial Analytics & Investment Tools */}
        <div>
          <motion.h3 
            className="text-3xl font-bold mb-8 text-center"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6 }}
          >
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#e45619] to-[#dd6c1c]">Financial Analytics & Investment Tools</span>
          </motion.h3>
          <div className="grid grid-cols-1 gap-4">
  {analyticsTools.map((feature, index) => (
    <motion.div 
      key={index} 
      className="relative group overflow-hidden bg-gradient-to-br from-space-blue-900/40 via-space-blue-950/60 to-deep-black/80 backdrop-blur-md p-4 rounded-xl border border-gray-700 h-auto min-h-24 transition-transform duration-100 hover:scale-105 hover:border-electric-blue-400 cursor-pointer"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      whileHover={{ scale: 1.05, transition: { duration: 0.1 } }}
    >
      <div className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_center,rgba(109,40,217,0.5)_0%,transparent_70%)] opacity-0 transition-opacity duration-500 group-hover:opacity-100"></div>
      <div className="relative z-10 flex items-start space-x-3 h-full">
        <div className="w-8 h-8 bg-gradient-to-r from-electric-blue-500/30 to-deep-purple-600/30 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
          <feature.icon className="w-4 h-4 text-[#e45619] rounded-full animate-pulse group-hover:text-[#dd6c1c] transition-colors duration-300" />
        </div>
        <div className="flex-1">
          <h4 className="text-base font-semibold text-text-primary mb-2 leading-tight">{feature.title}</h4>
          <p className="text-text-muted text-sm leading-relaxed">{feature.description}</p>
        </div>
      </div>
    </motion.div>
  ))}
</div>

        </div>

        {/* Automated Trading and Investment Tools */}
        <div className="mt-16">
          <motion.h3 
            className="text-3xl font-bold mb-8 text-center"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6 }}
          >
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#e45619] to-[#dd6c1c]">Automated Trading and Investment Tools</span>
          </motion.h3>
          <div className="grid grid-cols-1 gap-4">
              {tradingInvestingTools.map((feature, index) => (
                  <motion.div 
                      key={index} 
                      className="relative group overflow-hidden bg-gradient-to-br from-space-blue-900/40 via-space-blue-950/60 to-deep-black/80 backdrop-blur-md p-4 rounded-xl border border-gray-700 h-auto min-h-24 transition-transform duration-100 hover:scale-105 hover:border-electric-blue-400 cursor-pointer"
                      initial={{ opacity: 0, y: 50 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true, amount: 0.2 }}
                      transition={{ duration: 0.6, delay: index * 0.1 }}
                      whileHover={{ scale: 1.05, transition: { duration: 0.1 } }}
                  >
                      <div className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_center,rgba(109,40,217,0.5)_0%,transparent_70%)] opacity-0 transition-opacity duration-500 group-hover:opacity-100"></div>
                      <div className="relative z-10 flex items-start space-x-3 h-full">
                          <div className="w-8 h-8 bg-gradient-to-r from-electric-blue-500/30 to-deep-purple-600/30 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                              <feature.icon className="w-4 h-4 text-[#e45619] rounded-full animate-pulse group-hover:text-[#dd6c1c] transition-colors duration-300" />
                          </div>
                          <div className="flex-1">
                              <h4 className="text-base font-semibold text-text-primary mb-2 leading-tight">{feature.title}</h4>
                              <p className="text-text-muted text-sm leading-relaxed">{feature.description}</p>
                          </div>
                      </div>
                  </motion.div>
              ))}
          </div>
        </div>
        
      </div>
    </motion.section>
  );
};

export default Features;
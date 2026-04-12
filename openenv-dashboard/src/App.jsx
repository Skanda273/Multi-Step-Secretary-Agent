import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal, Copy, RotateCcw, Play, CheckCircle2, XCircle, Clock, ChevronRight, Activity, Code2, Layers, Cpu, Check, Save, Trophy, Star, Sparkles, Server } from 'lucide-react';

const mockRunAgent = async (task, currentState, onStep) => {
  await new Promise(r => setTimeout(r, 800));

  let empName = "John";
  let empDate = "Friday";
  let empTime = "3pm";

  const normalizedTask = task.trim();
  const fullMatch = normalizedTask.match(/(?:for|with)\s+(.+?)\s+on\s+(.+?)\s+at\s+(.+)$/i);
  const nameMatch = normalizedTask.match(/(?:for|with)\s+([A-Za-z][A-Za-z0-9 .'_-]+?)(?=\s+on|\s+at|$)/i);
  const dateMatch = normalizedTask.match(/on\s+([A-Za-z0-9\s,-]+)/i);
  const timeMatch = normalizedTask.match(/at\s+([0-9]{1,2}(?::[0-9]{2})?\s*(?:am|pm)?)/i);

  if (fullMatch) {
    empName = fullMatch[1].trim();
    empDate = fullMatch[2].trim();
    empTime = fullMatch[3].trim();
  } else {
    if (nameMatch) empName = nameMatch[1].trim();
    if (dateMatch) empDate = dateMatch[1].trim();
    if (timeMatch) empTime = timeMatch[1].trim();

    empName = empName || currentState.employee || "John";
    empDate = empDate || currentState.date || "Friday";
    empTime = empTime || currentState.time || "3pm";
  }

  const employeeId = `EMP_${empName.toUpperCase().replace(/\s+/g, '_')}_123`;

  const steps = [
    { name: 'Get_Employee_ID', args: { name: empName }, duration: '120ms', success: true, reward: 10 },
    { name: 'Check_Calendar', args: { employee_id: employeeId, date: empDate }, duration: '340ms', success: true, reward: 15 },
    { name: 'Book_Meeting', args: { employee_id: employeeId, time: empTime }, duration: '450ms', success: true, reward: 25 },
  ];

  const states = [
    { ...currentState, employee: empName, employee_id: null, date: empDate, calendar_checked: false, meeting_booked: false },
    { ...currentState, employee: empName, employee_id: employeeId, date: empDate, calendar_checked: false, meeting_booked: false },
    { ...currentState, employee: empName, employee_id: employeeId, date: empDate, calendar_checked: true, meeting_booked: false },
    { ...currentState, employee: empName, employee_id: employeeId, date: empDate, calendar_checked: true, meeting_booked: true }
  ];

  for (let i = 0; i < steps.length; i++) {
    onStep({
      step: steps[i],
      state: states[i + 1]
    });
    await new Promise(r => setTimeout(r, 1400));
  }

  return {
    status: 'success',
    message: `"${task}" executed successfully`
  };
};

// Shimmer Effect Component for Buttons
const Shimmer = () => (
  <motion.div
    className="absolute inset-0 -translate-x-[150%] bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-[-20deg]"
    animate={{ translateX: ['-150%', '150%'] }}
    transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
  />
);

function App() {
  const [task, setTask] = useState('Book meeting for John on Friday at 3pm');
  const [isRunning, setIsRunning] = useState(false);
  const [envState, setEnvState] = useState({
    employee: "John",
    employee_id: null,
    date: "Friday",
    calendar_checked: false,
    meeting_booked: false
  });
  const [executedSteps, setExecutedSteps] = useState([]);
  const [finalResult, setFinalResult] = useState(null);
  const [totalReward, setTotalReward] = useState(0);
  const [copied, setCopied] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const stateViewerRef = useRef(null);

  // Auto-scroll steps viewer
  const stepsContainerRef = useRef(null);
  useEffect(() => {
    if (stepsContainerRef.current) {
      stepsContainerRef.current.scrollTop = stepsContainerRef.current.scrollHeight;
    }
  }, [executedSteps, isRunning]);

  const handleRun = async () => {
    if (!task) return;
    setIsRunning(true);
    setExecutedSteps([]);
    setFinalResult(null);
    setTotalReward(0);

    const startingState = {
      ...envState,
      employee_id: null,
      calendar_checked: false,
      meeting_booked: false
    };
    setEnvState(startingState);

    try {
      const result = await mockRunAgent(task, startingState, ({ step, state }) => {
        setExecutedSteps(prev => [...prev, step]);
        setEnvState(state);
        setTotalReward(prev => prev + (step.reward || 0));
      });
      setFinalResult(result);
    } catch (err) {
      setFinalResult({ status: 'failed', message: 'Agent encountered a critical error.' });
    } finally {
      setIsRunning(false);
    }
  };

  const handleReset = () => {
    setTask('');
    setExecutedSteps([]);
    setFinalResult(null);
    setTotalReward(0);
    setEnvState({
      employee: "",
      employee_id: "",
      date: "",
      calendar_checked: false,
      meeting_booked: false
    });
  };

  const copyResult = () => {
    if (finalResult) {
      navigator.clipboard.writeText(JSON.stringify(finalResult, null, 2));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 font-sans p-4 sm:p-6 lg:p-8 flex flex-col relative overflow-hidden selection:bg-indigo-500/30 selection:text-indigo-200">

      {/* --- Premium Background Effects --- */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-indigo-600/10 mix-blend-screen blur-[120px] animate-pulse" style={{ animationDuration: '8s' }} />
        <div className="absolute top-[20%] right-[-10%] w-[40%] h-[40%] rounded-full bg-emerald-600/10 mix-blend-screen blur-[120px] animate-pulse" style={{ animationDuration: '12s' }} />
        <div className="absolute bottom-[-10%] left-[20%] w-[60%] h-[40%] rounded-full bg-blue-600/10 mix-blend-screen blur-[150px] animate-pulse" style={{ animationDuration: '10s' }} />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] mix-blend-overlay"></div>
        {/* Subtle grid pattern for technical feel */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]"></div>
      </div>

      {/* --- Top Header --- */}
      <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 mb-8 border-b border-indigo-500/10 pb-6 relative z-10 w-full max-w-7xl mx-auto">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="absolute inset-0 bg-indigo-500 blur-lg opacity-40 rounded-full animate-pulse"></div>
            <div className="relative h-14 w-14 rounded-2xl bg-gradient-to-br from-indigo-500 via-blue-500 to-cyan-400 p-[1px]">
              <div className="w-full h-full bg-slate-950 rounded-2xl flex items-center justify-center">
                <Server className="w-7 h-7 text-indigo-400" />
              </div>
            </div>
          </div>
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-200 to-indigo-400 drop-shadow-sm">
              OpenEnv Workspace
            </h1>
            <div className="flex items-center gap-2 mt-1.5">
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <p className="text-sm text-indigo-200/60 font-medium tracking-wide uppercase letter-spacing-1">Agent Status: Active</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 bg-slate-900/50 backdrop-blur-xl border border-white/5 rounded-2xl p-2 px-4 shadow-xl">
          <Trophy className="w-5 h-5 text-amber-400" />
          <div className="flex flex-col">
            <span className="text-[10px] text-slate-400 uppercase tracking-wider font-bold">Session Reward</span>
            <span className="text-lg font-bold text-amber-400 leading-none">{totalReward} pts</span>
          </div>
        </div>
      </header>

      {/* --- Main Dashboard --- */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 w-full max-w-7xl mx-auto pb-8 z-10">

        {/* LEFT COLUMN: Task Input & Agent Progress */}
        <div className="lg:col-span-4 flex flex-col gap-6">

          {/* Module: Instruction */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
            className="group relative bg-slate-900/40 border border-white/5 rounded-3xl backdrop-blur-xl shadow-2xl flex flex-col overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

            <div className="p-6 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-400">
                  <Terminal className="w-5 h-5" />
                </div>
                <h2 className="text-lg font-semibold text-white tracking-wide">Command Center</h2>
              </div>
            </div>

            <div className="p-6 flex flex-col gap-5 relative z-10">
              <div className="flex flex-col gap-2">
                <label className="text-xs font-semibold text-indigo-300/70 uppercase tracking-wider">Instruction Directive</label>
                <div className="relative group/input">
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 to-cyan-500 rounded-xl opacity-0 group-focus-within/input:opacity-30 blur transition duration-500"></div>
                  <textarea
                    value={task}
                    onChange={(e) => setTask(e.target.value)}
                    className="relative w-full h-28 bg-slate-950/80 border border-slate-800 rounded-xl p-4 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500/50 resize-none transition-all duration-300 shadow-inner"
                    placeholder="Describe the task for the autonomous agent..."
                  />
                  <div className="absolute bottom-3 right-3 text-slate-500 flex items-center gap-1">
                    <Sparkles className="w-4 h-4" />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 mt-2">
                <button
                  onClick={handleRun}
                  disabled={isRunning || !task}
                  className="relative overflow-hidden group bg-white text-slate-950 hover:bg-slate-100 disabled:bg-slate-800 disabled:text-slate-500 font-bold rounded-xl px-4 py-3.5 transition-all duration-300 flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(255,255,255,0.3)] disabled:shadow-none"
                >
                  {isRunning ? (
                    <>
                      <Activity className="w-5 h-5 animate-pulse text-indigo-500" />
                      <span>Executing...</span>
                      <Shimmer />
                      <motion.div
                        className="absolute bottom-0 left-0 h-1 bg-indigo-500"
                        initial={{ width: "0%" }}
                        animate={{ width: "100%" }}
                        transition={{ duration: 4, ease: "linear" }}
                      />
                    </>
                  ) : (
                    <>
                      <Play className="w-5 h-5" />
                      <span>Launch Agent</span>
                    </>
                  )}
                </button>
                <button
                  onClick={handleReset}
                  disabled={isRunning}
                  className="bg-slate-800/50 hover:bg-slate-700/80 border border-white/5 disabled:opacity-50 text-slate-300 font-semibold rounded-xl px-4 py-3.5 transition-all duration-300 flex items-center justify-center gap-2"
                >
                  <RotateCcw className="w-4 h-4" />
                  Reset
                </button>
              </div>
            </div>
          </motion.div>

          {/* Module: Final Result Output */}
          <AnimatePresence>
            {finalResult && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 10 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 10 }}
                className={`relative overflow-hidden rounded-3xl p-6 backdrop-blur-xl shadow-2xl flex flex-col gap-4 border ${finalResult.status === 'success'
                    ? 'bg-emerald-950/20 border-emerald-500/20'
                    : 'bg-rose-950/20 border-rose-500/20'
                  }`}
              >
                {/* Glow behind result */}
                <div className={`absolute top-0 right-0 w-32 h-32 blur-3xl opacity-20 ${finalResult.status === 'success' ? 'bg-emerald-500' : 'bg-rose-500'}`} />

                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-2xl ${finalResult.status === 'success'
                      ? 'bg-gradient-to-br from-emerald-500 to-emerald-700 text-white shadow-lg shadow-emerald-500/20'
                      : 'bg-gradient-to-br from-rose-500 to-rose-700 text-white shadow-lg shadow-rose-500/20'
                    }`}>
                    {finalResult.status === 'success' ? <CheckCircle2 className="w-6 h-6" /> : <XCircle className="w-6 h-6" />}
                  </div>
                  <div className="flex-1">
                    <h3 className={`text-lg font-bold ${finalResult.status === 'success' ? 'text-emerald-400' : 'text-rose-400'
                      }`}>
                      {finalResult.status === 'success' ? 'Mission Accomplished' : 'Mission Failed'}
                    </h3>
                    <p className="text-slate-300 text-sm mt-1 mb-4 leading-relaxed">{finalResult.message}</p>

                    <button
                      onClick={copyResult}
                      className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition-all ${finalResult.status === 'success'
                          ? 'bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/20'
                          : 'bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/20'
                        }`}
                    >
                      {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                      {copied ? 'LOG COPIED' : 'COPY LOG'}
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

        </div>

        {/* CENTER COLUMN: Environment State Editor */}
        <div className="lg:col-span-4 flex flex-col h-full">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="flex-1 bg-slate-900/40 border border-white/5 rounded-3xl backdrop-blur-xl shadow-2xl flex flex-col relative overflow-hidden group"
          >
            <div className="p-6 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-400">
                  <Layers className="w-5 h-5" />
                </div>
                <h2 className="text-lg font-semibold text-white tracking-wide">Environment Context</h2>
              </div>
            </div>

            <div className="flex-1 flex flex-col relative p-4">
              {/* macOS style editor window */}
              <div className="flex-1 bg-[#090b14] rounded-2xl border border-slate-800 flex flex-col shadow-inner overflow-hidden relative">

                {/* Editor Header */}
                <div className="h-10 bg-slate-900/80 border-b border-slate-800 flex items-center px-4 justify-between">
                  <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-rose-500/80"></div>
                    <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
                    <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
                  </div>
                  <div className="flex items-center gap-2 text-slate-500 text-xs font-medium">
                    <Code2 className="w-3.5 h-3.5" /> state.json
                  </div>
                  <button
                    onClick={() => { setIsSaved(true); setTimeout(() => setIsSaved(false), 2000); }}
                    disabled={isRunning}
                    className="text-slate-400 hover:text-emerald-400 transition-colors disabled:opacity-50"
                  >
                    {isSaved ? <Check className="w-4 h-4" /> : <Save className="w-4 h-4" />}
                  </button>
                </div>

                {/* Editor Body */}
                <div className="flex-1 overflow-auto p-4 space-y-5 font-mono text-sm custom-scrollbar relative">

                  {/* Subtle code lines background */}
                  <div className="absolute left-0 top-0 bottom-0 w-8 bg-slate-900/30 border-r border-slate-800/50 flex flex-col items-center py-4 text-slate-700 text-xs select-none pointer-events-none">
                    {Array.from({ length: 20 }).map((_, i) => <div key={i} className="mb-5">{i + 1}</div>)}
                  </div>

                  <div className="pl-6 space-y-4">
                    {/* Employee */}
                    <div className="group/field relative">
                      <div className="flex flex-col gap-1">
                        <span className="text-purple-400">"employee"<span className="text-slate-500">:</span></span>
                        <input
                          type="text"
                          disabled={isRunning}
                          value={envState.employee || ''}
                          onChange={(e) => setEnvState({ ...envState, employee: e.target.value })}
                          className="w-full bg-slate-950/50 border border-transparent hover:border-slate-800 rounded px-2 py-1 text-amber-300 focus:outline-none focus:border-indigo-500/50 focus:bg-indigo-500/5 disabled:opacity-60 transition-all font-mono"
                          placeholder="null"
                        />
                      </div>
                    </div>

                    {/* Employee ID */}
                    <div className="group/field relative">
                      <div className="flex flex-col gap-1">
                        <span className="text-purple-400">"employee_id"<span className="text-slate-500">:</span></span>
                        <input
                          type="text"
                          disabled={isRunning}
                          value={envState.employee_id || ''}
                          onChange={(e) => setEnvState({ ...envState, employee_id: e.target.value })}
                          className="w-full bg-slate-950/50 border border-transparent hover:border-slate-800 rounded px-2 py-1 text-amber-300 focus:outline-none focus:border-indigo-500/50 focus:bg-indigo-500/5 disabled:opacity-60 transition-all font-mono"
                          placeholder="null"
                        />
                      </div>
                    </div>

                    {/* Date */}
                    <div className="group/field relative">
                      <div className="flex flex-col gap-1">
                        <span className="text-purple-400">"date"<span className="text-slate-500">:</span></span>
                        <select
                          value={envState.date || ''}
                          disabled={isRunning}
                          onChange={(e) => setEnvState({ ...envState, date: e.target.value })}
                          className="w-full bg-slate-950/50 border border-transparent hover:border-slate-800 rounded px-2 py-1 text-amber-300 focus:outline-none focus:border-indigo-500/50 focus:bg-indigo-500/5 disabled:opacity-60 transition-all appearance-none font-mono cursor-pointer"
                        >
                          <option value="" className="text-slate-500">null</option>
                          {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].map(d => (
                            <option key={d} value={d}>"{d}"</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    {/* Calendar Bool */}
                    <div className="group/field relative flex items-center justify-between py-1 px-2 hover:bg-slate-800/30 rounded border border-transparent transition-colors">
                      <span className="text-purple-400">"calendar_checked"<span className="text-slate-500">:</span></span>
                      <button
                        type="button"
                        disabled={isRunning}
                        onClick={() => setEnvState({ ...envState, calendar_checked: !envState.calendar_checked })}
                        className="text-blue-400 hover:text-blue-300 focus:outline-none disabled:opacity-50"
                      >
                        {envState.calendar_checked ? 'true' : 'false'}
                      </button>
                    </div>

                    {/* Meeting Booked Bool */}
                    <div className="group/field relative flex items-center justify-between py-1 px-2 hover:bg-slate-800/30 rounded border border-transparent transition-colors">
                      <span className="text-purple-400">"meeting_booked"<span className="text-slate-500">:</span></span>
                      <button
                        type="button"
                        disabled={isRunning}
                        onClick={() => setEnvState({ ...envState, meeting_booked: !envState.meeting_booked })}
                        className="text-blue-400 hover:text-blue-300 focus:outline-none disabled:opacity-50"
                      >
                        {envState.meeting_booked ? 'true' : 'false'}
                      </button>
                    </div>

                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* RIGHT COLUMN: Real-time Execution Steps */}
        <div className="lg:col-span-4 flex flex-col h-full">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="flex-1 bg-slate-900/40 border border-white/5 rounded-3xl backdrop-blur-xl shadow-2xl flex flex-col overflow-hidden relative"
          >
            {/* Ambient Background Gradient for Steps */}
            <div className="absolute top-[20%] right-[-20%] w-[60%] h-[60%] bg-blue-600/10 rounded-full blur-[100px] pointer-events-none" />

            <div className="p-6 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-500/10 rounded-lg text-cyan-400">
                  <Cpu className="w-5 h-5" />
                </div>
                <h2 className="text-lg font-semibold text-white tracking-wide">Execution Path</h2>
              </div>
              <div className="px-3 py-1 bg-indigo-500/10 border border-indigo-500/20 rounded-full text-indigo-300 text-xs font-bold tracking-wider flex items-center gap-2">
                <Clock className="w-3 h-3" />
                LIVE
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar relative" ref={stepsContainerRef}>

              {/* Connecting vertical line */}
              {executedSteps.length > 0 && (
                <div className="absolute top-10 left-[39px] bottom-10 w-px bg-gradient-to-b from-blue-500/50 via-indigo-500/20 to-transparent -z-10"></div>
              )}

              {executedSteps.length === 0 && !isRunning && (
                <div className="h-full flex flex-col items-center justify-center text-slate-500/80 gap-4">
                  <div className="w-16 h-16 rounded-3xl border-2 border-dashed border-slate-700 flex items-center justify-center opacity-50">
                    <Activity className="w-6 h-6" />
                  </div>
                  <p className="text-sm font-medium tracking-wide">Awaiting Directive</p>
                </div>
              )}

              <AnimatePresence>
                {executedSteps.map((step, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -30, scale: 0.95 }}
                    animate={{ opacity: 1, x: 0, scale: 1 }}
                    className="relative"
                  >
                    {/* Circle Node */}
                    <div className="absolute -left-2 top-4 w-6 h-6 rounded-full bg-slate-900 border-4 border-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)] z-10 flex items-center justify-center">
                      {step.success && <div className="w-1.5 h-1.5 bg-white rounded-full"></div>}
                    </div>

                    <div className="ml-8 bg-slate-950/60 border border-white/5 rounded-2xl p-4 shadow-lg hover:border-blue-500/30 transition-colors group">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-bold text-white bg-blue-600 px-2.5 py-1 rounded-md shadow-sm">STEP {idx + 1}</span>
                          <h3 className="text-sm font-bold text-slate-200 group-hover:text-blue-300 transition-colors">{step.name}</h3>
                        </div>
                      </div>

                      {/* Arguments Box */}
                      <div className="bg-black/40 rounded-xl p-3 text-xs font-mono text-indigo-300/80 mb-3 border border-white/5">
                        <span className="text-slate-500 mb-1 block">// payload parameters</span>
                        {Object.entries(step.args).map(([k, v]) => (
                          <div key={k}><span className="text-blue-400">{k}</span>: <span className="text-amber-300">"{v}"</span></div>
                        ))}
                      </div>

                      {/* Footer Metrics */}
                      <div className="flex justify-between items-center text-xs font-bold font-mono">
                        <div className="flex items-center gap-1.5 text-amber-400 bg-amber-400/10 px-2 py-1 rounded-md border border-amber-400/10">
                          <Star className="w-3.5 h-3.5 fill-amber-400/50" />
                          +{step.reward} PTS
                        </div>
                        <div className="flex items-center gap-1.5 text-slate-400 bg-slate-800/50 px-2 py-1 rounded-md border border-white/5">
                          <Clock className="w-3.5 h-3.5" />
                          {step.duration}
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>

              {isRunning && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="ml-8 flex items-center p-4 bg-slate-950/40 rounded-2xl border border-dashed border-slate-700 shadow-sm relative overflow-hidden"
                >
                  <Shimmer />
                  <div className="flex items-center gap-3">
                    <div className="flex gap-1.5 items-center">
                      <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: '0ms' }} />
                      <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: '150ms' }} />
                      <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                    <span className="text-xs font-medium text-slate-400 tracking-wide">Processing current state...</span>
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>
        </div>

      </div>
    </div>
  );
}

export default App;

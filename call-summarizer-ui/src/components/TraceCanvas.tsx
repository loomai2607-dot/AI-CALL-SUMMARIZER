
import React, { useCallback, useState } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState
} from 'reactflow';
import 'reactflow/dist/style.css';

const TraceCanvas = ({ trace }: { trace: any[] }) => {
  const [selected, setSelected] = useState<any | null>(null);

  const nodes: any[] = trace.map((step, idx) => {
    const bgColor = step.status === 'success' ? '#e6ffed' : '#ffe6e6';
    return {
      id: String(idx),
      data: { label: step.name },
      position: { x: 100, y: idx * 120 },  // Vertical layout
      style: {
        padding: 10,
        border: '1px solid #ccc',
        borderRadius: 6,
        background: bgColor,
        minWidth: 120,
        textAlign: 'center'
      }
    };
  });

  const edges: any[] = trace.slice(1).map((_, idx) => ({
    id: `e${idx}-${idx + 1}`,
    source: String(idx),
    target: String(idx + 1),
    type: 'smoothstep'
  }));

  const [rfNodes, setNodes, onNodesChange] = useNodesState(nodes);
  const [rfEdges, setEdges, onEdgesChange] = useEdgesState(edges);

  const onNodeClick = useCallback((event: any, node: any) => {
    const index = parseInt(node.id);
    setSelected(trace[index]);
  }, [trace]);

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1 }}>
        <ReactFlow
          nodes={rfNodes}
          edges={rfEdges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          fitView
        >
          <Controls />
          <Background />
        </ReactFlow>
      </div>
      {selected && (
        <div style={{ padding: '1rem', borderTop: '1px solid #ccc', background: '#f9f9f9', maxHeight: 300, overflowY: 'auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <h4>Step: {selected.name}</h4>
            <button onClick={() => setSelected(null)} style={{ border: 'none', background: 'transparent', cursor: 'pointer' }}>❌</button>
          </div>
          <pre><strong>Status:</strong> {selected.status}</pre>
          <pre><strong>Input:</strong> {JSON.stringify(selected.input, null, 2)}</pre>
          <pre><strong>Output:</strong> {JSON.stringify(selected.output, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default TraceCanvas;

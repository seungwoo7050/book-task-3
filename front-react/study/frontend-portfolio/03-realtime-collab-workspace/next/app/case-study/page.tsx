export default function CaseStudyPage() {
  return (
    <main className="case-study-page">
      <div className="case-study-panel">
        <p className="eyebrow">Case Study</p>
        <h1>Realtime collaboration without a backend</h1>
        <p>
          This capstone keeps the collaboration story intentionally local. The
          interesting part is not deployment, but whether the UI can explain
          optimistic patches, presence, reconnect replay, and conflict surfaces
          in a way that still feels product-shaped.
        </p>
        <ul className="case-study-list">
          <li>Shared board cards update over a same-origin BroadcastChannel.</li>
          <li>Document blocks use the same patch envelope as the board.</li>
          <li>Disconnecting queues patches locally and replays them on reconnect.</li>
          <li>Editing the same entity from two tabs raises a visible conflict banner.</li>
        </ul>
      </div>
    </main>
  );
}

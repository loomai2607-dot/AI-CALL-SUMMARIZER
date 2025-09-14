
import React from 'react';

const FileUploadPreview = ({ file }: { file: File | null }) => {
  if (!file) return null;

  return (
    <div style={{ margin: '0.5rem 1rem', color: '#555' }}>
      <strong>Attached file:</strong> {file.name}
    </div>
  );
};

export default FileUploadPreview;

import React from 'react';
import { motion } from 'framer-motion';

export default function Section({ 
  id,
  icon: Icon,
  moduleNum,
  title,
  children,
  className = "" 
}) {
  return (
    <section id={id} className={`scroll-mt-24 max-w-7xl mx-auto px-4 w-full ${className}`}>
      
      {(Icon || title) && (
        <div className="mb-8 flex items-center gap-3 text-indigo-400">
          {Icon && <Icon size={28} />}
          <div>
            {moduleNum && (
              <div className="text-xs font-mono uppercase tracking-widest text-indigo-400">
                {moduleNum}
              </div>
            )}
            {title && (
              <h2 className="text-3xl font-black text-white">
                {title}
              </h2>
            )}
          </div>
        </div>
      )}

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.6 }}
        className="w-full"
      >
        {children}
      </motion.div>
    </section>
  );
}

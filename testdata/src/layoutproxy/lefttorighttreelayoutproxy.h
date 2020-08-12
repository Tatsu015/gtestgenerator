#ifndef LEFTTORIGHTTREELAYOUTPROXY_H
#define LEFTTORIGHTTREELAYOUTPROXY_H

#include "abstractlayoutproxy.h"
#include <QString>

class LeftToRightTreeLayoutProxy : public AbstractLayoutProxy {
public:
  const static QString NAME;

public:
  LeftToRightTreeLayoutProxy();
  virtual ~LeftToRightTreeLayoutProxy();

  virtual void layout(Node* rootNode);
  virtual QString name() const;

private:
  qreal layoutChild(const Node* node);
  qreal treeHeight(const Node* node);
  qreal childrenHeight(const Node* node);
  void drawConnection(const Node* parentNode, const Node* childNode);
};

#endif // LEFTTORIGHTTREELAYOUTPROXY_H

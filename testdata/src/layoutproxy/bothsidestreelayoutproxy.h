#ifndef BOTHSIDESTREELAYOUTPROXY_H
#define BOTHSIDESTREELAYOUTPROXY_H

#include "abstractlayoutproxy.h"
#include <QString>

class BothSidesTreeLayoutProxy : public AbstractLayoutProxy {
public:
  const static QString NAME;

public:
  BothSidesTreeLayoutProxy();
  virtual ~BothSidesTreeLayoutProxy();

  virtual void layout(Node* rootNode);
  virtual QString name() const;

private:
  qreal layoutChildFromLeftToRight(const Node* node);
  qreal layoutChildFromRightToLeft(const Node* node);
  qreal treeHeight(const Node* node);
  qreal childrenHeight(const Node* node);
  void drawConnectionLeftToRight(const Node* parentNode, const Node* childNode);
  void drawConnectionRightToLeft(const Node* parentNode, const Node* childNode);
  void shiftRightToLeftNodes(QList<Node*> nodes, const qreal x, const qreal y);
  void shiftLeftToRightNodes(QList<Node*> nodes, const qreal x, const qreal y);
};

#endif // BOTHSIDESTREELAYOUTPROXY_H
